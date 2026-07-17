"use client";

import { useEffect, useState } from "react";

import { getApiHealth } from "@/lib/api";

type HealthState = {
  loading: boolean;
  status: string;
  error: string | null;
};

export function useApiHealth() {
  const [health, setHealth] = useState<HealthState>({
    loading: true,
    status: "checking",
    error: null,
  });

  useEffect(() => {
    let isMounted = true;

    const run = async () => {
      try {
        const response = await getApiHealth();
        if (!isMounted) return;
        setHealth({ loading: false, status: response.status, error: null });
      } catch (err) {
        if (!isMounted) return;
        setHealth({
          loading: false,
          status: "offline",
          error: err instanceof Error ? err.message : "Unknown error",
        });
      }
    };

    run();
    return () => {
      isMounted = false;
    };
  }, []);

  return health;
}
