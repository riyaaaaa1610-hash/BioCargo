import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[11px] font-medium uppercase tracking-wider",
  {
    variants: {
      variant: {
        default: "border border-line bg-panel text-zinc-200",
        ok: "bg-ok/10 text-ok ring-1 ring-ok/30",
        signal: "bg-signal/10 text-signal ring-1 ring-signal/30",
        alert: "bg-alert/10 text-alert ring-1 ring-alert/30",
        frost: "bg-frost/10 text-frost ring-1 ring-frost/30",
        outline: "border border-line text-zinc-200",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
