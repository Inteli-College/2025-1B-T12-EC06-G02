import * as React from "react";
import { Slot } from "@radix-ui/react-slot";

function Button({ className, variant = "primary", size = "default", color, asChild = false, ...props }) {
  const Comp = asChild ? Slot : "button";

  const baseStyles =
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded text-lg font-medium transition-colors disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-5 shrink-0 [&_svg]:shrink-0 outline-none focus-visible:ring-2 focus-visible:ring-offset-2";

  const variantStyles = {
    primary: "bg-[#2d608d] text-white hover:bg-[#245179]",
    success: "bg-[#204565] text-white hover:bg-[#19354F]",
    outline: "border bg-white text-gray-700 hover:bg-gray-100",
  };

  const sizeStyles = {
    default: "h-12 px-4 py-2",
    sm: "h-10 px-3 py-1.5",
    lg: "h-14 px-6 py-3",
  };

  const customColorStyles = color
    ? `bg-[${color}] text-white hover:bg-opacity-90`
    : "";

  const combinedStyles = `${baseStyles} ${customColorStyles || variantStyles[variant]} ${sizeStyles[size]} ${className || ""}`;

  return <Comp data-slot="button" className={combinedStyles} {...props} />;
}

export { Button };
