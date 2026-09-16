import {
  useQuery,
  useMutation,
  useQueryClient,
  type UseQueryOptions,
} from "@tanstack/react-query";
import {
  getCargo,
  getCargoById,
  createCargo,
  updateCargo,
  deleteCargo,
  type CargoRecord,
  type CargoInput,
  type CargoUpdateInput,
} from "@/lib/api";

const cargoKeys = {
  all: ["cargo"] as const,
  list: () => [...cargoKeys.all, "list"] as const,
  detail: (id: string) => [...cargoKeys.all, "detail", id] as const,
};

export function useCargoList(
  options?: Omit<UseQueryOptions<CargoRecord[], Error>, "queryKey" | "queryFn">,
) {
  return useQuery<CargoRecord[], Error>({
    queryKey: cargoKeys.list(),
    queryFn: getCargo,
    ...options,
  });
}

export function useCargoById(id: string) {
  return useQuery<CargoRecord, Error>({
    queryKey: cargoKeys.detail(id),
    queryFn: () => getCargoById(id),
    enabled: !!id,
  });
}

export function useCreateCargo() {
  const queryClient = useQueryClient();
  return useMutation<CargoRecord, Error, CargoInput>({
    mutationFn: createCargo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: cargoKeys.list() });
    },
  });
}

export function useUpdateCargo() {
  const queryClient = useQueryClient();
  return useMutation<CargoRecord, Error, { id: string; cargo: CargoUpdateInput }>({
    mutationFn: ({ id, cargo }) => updateCargo(id, cargo),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: cargoKeys.list() });
      queryClient.invalidateQueries({ queryKey: cargoKeys.detail(variables.id) });
    },
  });
}

export function useDeleteCargo() {
  const queryClient = useQueryClient();
  return useMutation<void, Error, string>({
    mutationFn: deleteCargo,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: cargoKeys.list() });
    },
  });
}
