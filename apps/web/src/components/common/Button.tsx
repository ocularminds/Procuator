"use client";

import type { ButtonHTMLAttributes } from "react";

export function Button(props: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      {...props}
      className={
        "rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black shadow-lg shadow-white/10 hover:bg-white/90 disabled:cursor-not-allowed disabled:opacity-50 " +
        (props.className ?? "")
      }
    />
  );
}
