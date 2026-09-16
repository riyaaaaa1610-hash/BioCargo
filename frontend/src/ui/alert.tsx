import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const alertVariants = cva(
  "relative flex items-start gap-3 rounded-lg p-3 text-sm [&>svg]:h-4 [&>svg]:w-4",
  {
    variants: {
      variant: {
        default: "bg-panel-2 text-zinc-200 ring-1 ring-line",
        alert: "bg-alert/10 text-alert ring-1 ring-alert/30",
        signal: "bg-signal/10 text-signal ring-1 ring-signal/30",
        ok: "bg-ok/10 text-ok ring-1 ring-ok/30",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

export interface AlertProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof alertVariants> {}

function Alert({ className, variant, ...props }: AlertProps) {
  return (
    <div
      role="alert"
      className={cn(alertVariants({ variant }), className)}
      {...props}
    />
  );
}

export { Alert, alertVariants };
