import { useMutation } from "@tanstack/react-query";
import { predictCargo, type PredictRequest, type PredictResponse } from "@/lib/api";

export function usePredict() {
  return useMutation<PredictResponse, Error, PredictRequest>({
    mutationFn: predictCargo,
  });
}
