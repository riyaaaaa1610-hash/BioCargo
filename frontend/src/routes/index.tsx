import { useState, useMemo, useEffect } from "react";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { cn } from "@/lib/utils";
import { usePredict } from "@/hooks/use-predict";
import {
  useCargoList,
  useCreateCargo,
  useUpdateCargo,
  useDeleteCargo,
} from "@/hooks/use-cargo";
import type { CargoRecord, PredictResponse } from "@/lib/api";
import { Button } from "@/ui/button";
import { Input } from "@/ui/input";
import { Label } from "@/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/ui/select";
import { Badge } from "@/ui/badge";
import { Alert } from "@/ui/alert";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogTrigger,
} from "@/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/ui/table";
import { Skeleton } from "@/ui/skeleton";
import {
  AlertCircle,
  ArrowRight,
  Beaker,
  Box,
  Edit2,
  Loader2,
  Plus,
  RefreshCw,
  Thermometer,
  Timer,
  Trash2,
} from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "bioCargo — Synthetic Biology Cargo Viability" },
      {
        name: "description",
        content:
          "Monitor synthetic biology cargo viability with Arrhenius and ML predictions for aviation cold-chain shipments.",
      },
      {
        property: "og:title",
        content: "bioCargo — Synthetic Biology Cargo Viability",
      },
      {
        property: "og:description",
        content:
          "Monitor synthetic biology cargo viability with Arrhenius and ML predictions for aviation cold-chain shipments.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: Index,
});

const emptyForm = {
  cargo_id: "",
  cargo_type: "",
  current_temp: "",
  flight_duration_hours: "",
  flight_delay_minutes: "",
};

function Index() {
  const navigate = useNavigate();
  useEffect(()=>{ if(!sessionStorage.getItem('biocargo_user')) navigate({to:'/login'});},[navigate]);
  const [form, setForm] = useState(emptyForm);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const predict = usePredict();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setResult(null);
    predict.mutate(
      {
        cargo_type: form.cargo_type,
        current_temp: Number(form.current_temp),
        flight_duration_hours: Number(form.flight_duration_hours),
        flight_delay_minutes: Number(form.flight_delay_minutes),
      },
      {
        onSuccess: (data) => setResult(data),
      },
    );
  };

  return (
    <div className="min-h-screen bg-background font-sans antialiased">
      <Header />

      <main className="mx-auto max-w-[1200px] px-4 py-6 sm:px-6">
        <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-frost-dim">
              Prediction Console
            </p>
            <h1 className="mt-1.5 text-3xl font-semibold tracking-tight text-zinc-50 text-balance">
              Viability telemetry
            </h1>
          </div>
          {result && (
            <Badge variant={riskBadgeVariant(result.risk_level)}>
              <span className="pulse-dot size-1.5 rounded-full bg-current" />
              {result.risk_level}
            </Badge>
          )}
        </div>

        <div className="grid gap-5 lg:grid-cols-[340px_1fr]">
          <PredictionForm
            form={form}
            setForm={setForm}
            isPending={predict.isPending}
            onSubmit={handleSubmit}
          />
          <ResultsPanel
            result={result}
            cargoId={form.cargo_id}
            isPending={predict.isPending}
            error={predict.error}
          />
        </div>

        <CargoRegistry />
      </main>
    </div>
  );
}

function Header() {
  const { data: cargo, isLoading, isError } = useCargoList({ retry: false });
  const apiOnline = !isError;

  const criticalCount = useMemo(() => {
    if (!cargo) return 0;
    return cargo.filter(
      (c) =>
        c.risk_level?.toLowerCase().includes("critical") ||
        c.risk_level?.toLowerCase().includes("high"),
    ).length;
  }, [cargo]);

  return (
    <header className="border-b border-line">
      <div className="mx-auto flex h-14 max-w-[1200px] items-center gap-4 px-4 sm:px-6">
        <div className="flex items-center gap-2.5">
          <div className="grid size-8 place-items-center rounded-lg bg-frost/15 ring-1 ring-frost/30">
            <Beaker className="size-4 text-frost" />
          </div>
          <div className="leading-none">
            <p className="text-[15px] font-semibold tracking-tight text-zinc-100">
              bioCargo
            </p>
            <p className="mt-1 font-mono text-[10px] tracking-wide text-muted-foreground">
              SYNBIO CARGO VIABILITY
            </p>
          </div>
        </div>

        <div className="ml-auto flex items-center gap-3">
          <div className="flex items-center gap-2 rounded-md bg-panel px-3 py-1.5 ring-1 ring-line">
            <span
              className={cn(
                "pulse-dot size-1.5 rounded-full",
                apiOnline ? "bg-ok" : "bg-alert",
              )}
            />
            <span className="font-mono text-[11px] text-muted-foreground">
              {isLoading ? "Checking API…" : apiOnline ? "API Online" : "API Offline"}
            </span>
          </div>
          {criticalCount > 0 && (
            <Badge variant="alert" className="hidden sm:inline-flex">
              {criticalCount} critical
            </Badge>
          )}
          <div className="grid size-8 place-items-center rounded-full bg-frost/15 ring-1 ring-frost/30">
            <button onClick={()=>{sessionStorage.clear(); window.location.href="/login";}} className="text-[10px] text-frost">OUT</button>
          </div>
        </div>
      </div>
    </header>
  );
}

interface PredictionFormProps {
  form: typeof emptyForm;
  setForm: React.Dispatch<React.SetStateAction<typeof emptyForm>>;
  isPending: boolean;
  onSubmit: (e: React.FormEvent) => void;
}

function PredictionForm({
  form,
  setForm,
  isPending,
  onSubmit,
}: PredictionFormProps) {
  const update = (field: keyof typeof form, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  return (
    <section className="space-y-4 rounded-xl bg-panel p-5 ring-1 ring-line">
      <div className="flex items-center justify-between">
        <h2 className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
          New Reading
        </h2>
        <span className="font-mono text-[10px] text-frost-dim">POST /predict</span>
      </div>

      <form onSubmit={onSubmit} className="space-y-4">
        <div>
          <Label htmlFor="cargo_id">Cargo ID</Label>
          <Input
            id="cargo_id"
            placeholder="SBC-2291"
            value={form.cargo_id}
            onChange={(e) => update("cargo_id", e.target.value)}
            className="mt-1.5 font-mono"
          />
        </div>

        <div>
          <Label htmlFor="cargo_type">Cargo Type</Label>
          <Select
            value={form.cargo_type}
            onValueChange={(value) => update("cargo_type", value)}
          >
            <SelectTrigger className="mt-1.5">
              <SelectValue placeholder="Select cargo type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="Solid Organs">Solid Organs</SelectItem>
              <SelectItem value="Platelets">Platelets</SelectItem>
              <SelectItem value="Red Blood Cells">Red Blood Cells</SelectItem>
              <SelectItem value="Plasma & Cryo">Plasma & Cryo</SelectItem>
              <SelectItem value="Skin, Bones, Valves">Skin, Bones, Valves</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <Label htmlFor="current_temp">Temp °C</Label>
            <Input
              id="current_temp"
              type="number"
              step="0.1"
              placeholder="7.2"
              value={form.current_temp}
              onChange={(e) => update("current_temp", e.target.value)}
              className="mt-1.5 font-mono"
            />
          </div>
          <div>
            <Label htmlFor="flight_duration_hours">Duration h</Label>
            <Input
              id="flight_duration_hours"
              type="number"
              step="0.1"
              placeholder="11"
              value={form.flight_duration_hours}
              onChange={(e) => update("flight_duration_hours", e.target.value)}
              className="mt-1.5 font-mono"
            />
          </div>
        </div>

        <div>
          <Label htmlFor="flight_delay_minutes">Delay (min)</Label>
          <Input
            id="flight_delay_minutes"
            type="number"
            placeholder="45"
            value={form.flight_delay_minutes}
            onChange={(e) => update("flight_delay_minutes", e.target.value)}
            className="mt-1.5 font-mono"
          />
        </div>

        <Button
          type="submit"
          disabled={isPending}
          className="w-full bg-frost text-ink hover:bg-frost/90"
        >
          {isPending ? (
            <>
              <Loader2 className="size-4 animate-spin" />
              Computing…
            </>
          ) : (
            <>
              Run prediction
              <ArrowRight className="size-4" />
            </>
          )}
        </Button>
      </form>
    </section>
  );
}

interface ResultsPanelProps {
  result: PredictResponse | null;
  cargoId: string;
  isPending: boolean;
  error: Error | null;
}

function ResultsPanel({ result, cargoId, isPending, error }: ResultsPanelProps) {
  if (isPending) {
    return <ResultsSkeleton />;
  }

  if (error) {
    return (
      <Alert variant="alert">
        <AlertCircle className="mt-0.5 shrink-0" />
        <div>
          <p className="font-medium">Prediction failed</p>
          <p className="mt-1 font-mono text-[11px] text-current/70">
            {error.message} — check that the Flask backend is running at
            127.0.0.1:5000.
          </p>
        </div>
      </Alert>
    );
  }

  if (!result) {
    return (
      <div className="flex min-h-[320px] flex-col items-center justify-center rounded-xl bg-panel p-6 ring-1 ring-line text-center">
        <Box className="size-10 text-frost-dim" />
        <p className="mt-4 text-sm text-zinc-300">No prediction run yet.</p>
        <p className="mt-1 text-xs text-muted-foreground">
          Enter cargo parameters and run POST /predict to see viability metrics.
        </p>
      </div>
    );
  }

  const delta = result.arrhenius_viability - result.ml_viability;

  return (
    <section className="grid grid-cols-2 gap-4">
      <div className="col-span-2 flex items-end justify-between rounded-xl bg-panel p-5 ring-1 ring-line">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
            Arrhenius Viability
          </p>
          <p className="mt-2 text-5xl font-semibold leading-none tracking-tight text-frost md:text-6xl">
            {result.arrhenius_viability.toFixed(1)}
            <i className="align-top text-2xl text-frost-dim">%</i>
          </p>
        </div>
        <div className="text-right">
          <p className="font-mono text-[11px] text-muted-foreground">
            ML Viability
          </p>
          <p className="mt-1 text-3xl font-semibold leading-none text-zinc-100">
            {result.ml_viability.toFixed(1)}%
          </p>
          <p className="mt-1.5 font-mono text-[10px] text-frost-dim">
            {delta >= 0 ? "+" : ""}
            {delta.toFixed(1)} pts delta
          </p>
        </div>
      </div>

      <MetricCard label="Risk Level" value={result.risk_level}>
        <span
          className={cn(
            "pulse-dot size-2 rounded-full",
            riskDotColor(result.risk_level),
          )}
        />
      </MetricCard>

      <MetricCard label="Temperature Status" value={result.temperature_status}>
        <Thermometer className="size-5 text-frost" />
      </MetricCard>

      <MetricCard
        label="Safe Time Left"
        value={`${result.time_remaining_hours.toFixed(1)}`}
        unit="h"
        valueClass="text-ok"
        icon={<Timer className="size-5 text-ok" />}
      />

      <MetricCard
        label="Total Exposure"
        value={`${result.total_exposure_hours.toFixed(1)}`}
        unit="h"
        icon={<RefreshCw className="size-5 text-zinc-400" />}
      />

      <div className="col-span-2 rounded-xl bg-panel p-4 ring-1 ring-line">
        <div className="flex items-end justify-between gap-4">
          <div>
            <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
              Degradation Rate
            </p>
            <p className="mt-1 text-2xl font-semibold leading-none tracking-tight text-signal">
              {result.degradation_rate.toFixed(3)}{" "}
              <span className="font-mono text-sm text-muted-foreground">per h</span>
            </p>
          </div>
          <div className="w-40">
            <div className="h-1.5 overflow-hidden rounded-full bg-panel-2">
              <div
                className="h-full rounded-full bg-signal"
                style={{ width: `${Math.min(result.degradation_rate * 1000, 100)}%` }}
              />
            </div>
            <p className="mt-1.5 text-right font-mono text-[10px] text-muted-foreground">
              Rate indicator
            </p>
          </div>
        </div>
      </div>

      {cargoId && (
        <div className="col-span-2 rounded-lg bg-panel-2 px-3 py-2 ring-1 ring-line">
          <p className="font-mono text-[10px] text-muted-foreground">
            Reference ID: <span className="text-zinc-200">{cargoId}</span>
          </p>
        </div>
      )}
    </section>
  );
}

function MetricCard({
  label,
  value,
  unit,
  valueClass,
  children,
  icon,
}: {
  label: string;
  value: string | number;
  unit?: string;
  valueClass?: string;
  children?: React.ReactNode;
  icon?: React.ReactNode;
}) {
  return (
    <div className="rounded-xl bg-panel p-4 ring-1 ring-line">
      <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
        {label}
      </p>
      <div className="mt-2 flex items-center gap-2">
        {children || icon}
        <span className={cn("text-2xl font-semibold tracking-tight", valueClass)}>
          {value}
          {unit && (
            <i className="ml-1 text-base text-muted-foreground">{unit}</i>
          )}
        </span>
      </div>
    </div>
  );
}

function ResultsSkeleton() {
  return (
    <div className="grid grid-cols-2 gap-4">
      <Skeleton className="col-span-2 h-36 rounded-xl" />
      <Skeleton className="h-28 rounded-xl" />
      <Skeleton className="h-28 rounded-xl" />
      <Skeleton className="h-28 rounded-xl" />
      <Skeleton className="h-28 rounded-xl" />
      <Skeleton className="col-span-2 h-24 rounded-xl" />
    </div>
  );
}

function CargoRegistry() {
  const { data: cargo, isLoading, error, refetch } = useCargoList();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<CargoRecord | null>(null);

  return (
    <section className="mt-8">
      <div className="mb-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
            Cargo Registry
          </p>
          <h2 className="mt-1 text-xl font-semibold tracking-tight text-zinc-100">
            Active shipments
          </h2>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => refetch()}
            className="text-zinc-200"
          >
            <RefreshCw className="size-4" />
            Refresh
          </Button>
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button
                size="sm"
                className="bg-frost text-ink hover:bg-frost/90"
                onClick={() => setEditing(null)}
              >
                <Plus className="size-4" />
                Add cargo
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-lg">
              <DialogHeader>
                <DialogTitle>{editing ? "Edit cargo" : "Add cargo"}</DialogTitle>
                <DialogDescription>
                  {editing
                    ? "Update the cargo record in the registry."
                    : "Create a new cargo record for tracking."}
                </DialogDescription>
              </DialogHeader>
              <CargoForm
                initial={editing}
                onClose={() => setDialogOpen(false)}
              />
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="overflow-hidden rounded-xl bg-panel ring-1 ring-line">
        <div className="overflow-x-auto">
          <Table className="min-w-[720px]">
            <TableHeader>
              <TableRow>
                <TableHead>Cargo ID</TableHead>
                <TableHead>Type</TableHead>
                <TableHead className="text-right">Temp</TableHead>
                <TableHead>Duration</TableHead>
                <TableHead>Delay</TableHead>
                <TableHead>Risk</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                Array.from({ length: 4 }).map((_, i) => (
                  <TableRow key={i}>
                    {Array.from({ length: 8 }).map((_, j) => (
                      <TableCell key={j}>
                        <Skeleton className="h-4 w-full max-w-[80px]" />
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : error ? (
                <TableRow>
                  <TableCell colSpan={8}>
                    <Alert variant="alert">
                      <AlertCircle className="mt-0.5 shrink-0" />
                      <div>
                        <p className="font-medium">Registry unavailable</p>
                        <p className="mt-1 font-mono text-[11px] text-current/70">
                          {error.message}
                        </p>
                      </div>
                    </Alert>
                  </TableCell>
                </TableRow>
              ) : !cargo?.length ? (
                <TableRow>
                  <TableCell colSpan={8}>
                    <div className="py-8 text-center text-sm text-muted-foreground">
                      No cargo records found.
                    </div>
                  </TableCell>
                </TableRow>
              ) : (
                cargo.map((record) => (
                  <CargoRow
                    key={record.cargo_id}
                    record={record}
                    onEdit={() => {
                      setEditing(record);
                      setDialogOpen(true);
                    }}
                  />
                ))
              )}
            </TableBody>
          </Table>
        </div>
      </div>
    </section>
  );
}

function CargoRow({
  record,
  onEdit,
}: {
  record: CargoRecord;
  onEdit: () => void;
}) {
  const deleteCargo = useDeleteCargo();

  return (
    <TableRow>
      <TableCell className="font-mono text-zinc-200">{record.cargo_id}</TableCell>
      <TableCell className="text-zinc-300">{record.cargo_type}</TableCell>
      <TableCell className="text-right font-mono text-zinc-200">
        {record.current_temp}°C
      </TableCell>
      <TableCell className="font-mono text-zinc-300">
        {record.flight_duration_hours}h
      </TableCell>
      <TableCell className="font-mono text-zinc-300">
        {record.flight_delay_minutes}m
      </TableCell>
      <TableCell>
        <Badge variant={riskBadgeVariant(record.risk_level)}>
          {record.risk_level ? (
            <>
              <span
                className={cn(
                  "size-1.5 rounded-full",
                  riskDotColor(record.risk_level),
                  shouldPulse(record.risk_level) && "pulse-dot",
                )}
              />
              {record.risk_level}
            </>
          ) : (
            "—"
          )}
        </Badge>
      </TableCell>
      <TableCell className="font-mono text-[11px] uppercase text-muted-foreground">
        {record.temperature_status ?? "—"}
      </TableCell>
      <TableCell className="text-right">
        <div className="flex items-center justify-end gap-1">
          <Button
            variant="ghost"
            size="icon"
            className="size-8 text-muted-foreground hover:text-zinc-200"
            onClick={onEdit}
          >
            <Edit2 className="size-3.5" />
            <span className="sr-only">Edit</span>
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="size-8 text-muted-foreground hover:text-alert"
            onClick={() => deleteCargo.mutate(record.cargo_id)}
            disabled={deleteCargo.isPending}
          >
            {deleteCargo.isPending ? (
              <Loader2 className="size-3.5 animate-spin" />
            ) : (
              <Trash2 className="size-3.5" />
            )}
            <span className="sr-only">Delete</span>
          </Button>
        </div>
      </TableCell>
    </TableRow>
  );
}

function CargoForm({
  initial,
  onClose,
}: {
  initial: CargoRecord | null;
  onClose: () => void;
}) {
  const create = useCreateCargo();
  const update = useUpdateCargo();
  const [form, setForm] = useState({
    cargo_id: initial?.cargo_id ?? "",
    cargo_type: initial?.cargo_type ?? "",
    current_temp: initial?.current_temp?.toString() ?? "",
    flight_duration_hours: initial?.flight_duration_hours?.toString() ?? "",
    flight_delay_minutes: initial?.flight_delay_minutes?.toString() ?? "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      cargo_id: form.cargo_id,
      cargo_type: form.cargo_type,
      current_temp: Number(form.current_temp),
      flight_duration_hours: Number(form.flight_duration_hours),
      flight_delay_minutes: Number(form.flight_delay_minutes),
    };

    if (initial) {
      update.mutate(
        { id: initial.cargo_id, cargo: payload },
        { onSuccess: onClose },
      );
    } else {
      create.mutate(payload, { onSuccess: onClose });
    }
  };

  const updateField = (field: keyof typeof form, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const isPending = create.isPending || update.isPending;
  const error = create.error || update.error;

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label htmlFor="form_cargo_id">Cargo ID</Label>
        <Input
          id="form_cargo_id"
          placeholder="SBC-2291"
          value={form.cargo_id}
          disabled={!!initial}
          onChange={(e) => updateField("cargo_id", e.target.value)}
          className="mt-1.5 font-mono"
          required
        />
      </div>
      <div>
        <Label htmlFor="form_cargo_type">Cargo Type</Label>
        <Select
          value={form.cargo_type}
          onValueChange={(value) => updateField("cargo_type", value)}
        >
          <SelectTrigger className="mt-1.5">
            <SelectValue placeholder="Select cargo type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="Solid Organs">Solid Organs</SelectItem>
            <SelectItem value="Platelets">Platelets</SelectItem>
            <SelectItem value="Red Blood Cells">Red Blood Cells</SelectItem>
            <SelectItem value="Plasma & Cryo">Plasma & Cryo</SelectItem>
            <SelectItem value="Skin, Bones, Valves">Skin, Bones, Valves</SelectItem>
          </SelectContent>
        </Select>
      </div>
      <div className="grid grid-cols-2 gap-3">
        <div>
          <Label htmlFor="form_current_temp">Temp °C</Label>
          <Input
            id="form_current_temp"
            type="number"
            step="0.1"
            placeholder="7.2"
            value={form.current_temp}
            onChange={(e) => updateField("current_temp", e.target.value)}
            className="mt-1.5 font-mono"
            required
          />
        </div>
        <div>
          <Label htmlFor="form_duration">Duration h</Label>
          <Input
            id="form_duration"
            type="number"
            step="0.1"
            placeholder="11"
            value={form.flight_duration_hours}
            onChange={(e) => updateField("flight_duration_hours", e.target.value)}
            className="mt-1.5 font-mono"
            required
          />
        </div>
      </div>
      <div>
        <Label htmlFor="form_delay">Delay min</Label>
        <Input
          id="form_delay"
          type="number"
          placeholder="45"
          value={form.flight_delay_minutes}
          onChange={(e) => updateField("flight_delay_minutes", e.target.value)}
          className="mt-1.5 font-mono"
          required
        />
      </div>

      {error && (
        <Alert variant="alert">
          <AlertCircle className="mt-0.5 shrink-0" />
          <p className="font-medium">{error.message}</p>
        </Alert>
      )}

      <DialogFooter>
        <Button type="button" variant="outline" onClick={onClose}>
          Cancel
        </Button>
        <Button
          type="submit"
          disabled={isPending}
          className="bg-frost text-ink hover:bg-frost/90"
        >
          {isPending ? (
            <>
              <Loader2 className="size-4 animate-spin" />
              Saving…
            </>
          ) : initial ? (
            "Update cargo"
          ) : (
            "Create cargo"
          )}
        </Button>
      </DialogFooter>
    </form>
  );
}

function riskBadgeVariant(
  risk?: string,
): "default" | "ok" | "signal" | "alert" | "frost" {
  const r = risk?.toLowerCase() ?? "";
  if (r.includes("critical") || r.includes("high")) return "alert";
  if (r.includes("elevated") || r.includes("moderate") || r.includes("medium"))
    return "signal";
  if (r.includes("low") || r.includes("nominal") || r.includes("stable"))
    return "ok";
  return "default";
}

function riskDotColor(risk?: string): string {
  const variant = riskBadgeVariant(risk);
  switch (variant) {
    case "alert":
      return "bg-alert";
    case "signal":
      return "bg-signal";
    case "ok":
      return "bg-ok";
    case "frost":
      return "bg-frost";
    default:
      return "bg-muted-foreground";
  }
}

function shouldPulse(risk?: string): boolean {
  const r = risk?.toLowerCase() ?? "";
  return r.includes("critical") || r.includes("high") || r.includes("elevated");
}
