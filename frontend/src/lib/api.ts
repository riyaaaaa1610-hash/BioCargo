export interface PredictRequest {
  cargo_type: string;
  current_temp: number;
  flight_duration_hours: number;
  flight_delay_minutes: number;
}

export interface PredictResponse {
  arrhenius_viability: number;
  ml_viability: number;
  risk_level: string;
  temperature_status: string;
  time_remaining_hours: number;
  total_exposure_hours: number;
  degradation_rate: number;
}

export interface CargoRecord {
  cargo_id: string;
  cargo_type: string;
  current_temp: number;
  safe_temp: number;
  max_temp_threshold: number;
  flight_duration_hours: number;
  flight_delay_minutes: number;
  viability_percentage?: number;
  arrhenius_viability?: number;
  ml_viability?: number;
  risk_level?: string;
  temperature_status?: string;
  time_remaining_hours?: number;
  total_exposure_hours?: number;
  degradation_rate?: number;
}

export interface CargoInput {
  cargo_id: string;
  cargo_type: string;
  current_temp: number;
  flight_duration_hours: number;
  flight_delay_minutes: number;
}

export interface CargoUpdateInput {
  current_temp: number;
  flight_duration_hours: number;
  flight_delay_minutes: number;
}

interface ApiSuccess<T> {
  success: true;
  data: T;
}

interface ApiErrorResponse {
  success?: false;
  error?: string;
}

class ApiError extends Error {
  constructor(message: string, public status: number, public body?: unknown) {
    super(message);
    this.name = "ApiError";
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  let body: unknown;
  try {
    body = await response.json();
  } catch {
    body = await response.text().catch(() => null);
  }

  if (!response.ok) {
    const errorBody = body as ApiErrorResponse | null;
    throw new ApiError(
      errorBody?.error || `Request failed: ${response.status} ${response.statusText}`,
      response.status,
      body,
    );
  }

  const result = body as ApiSuccess<T>;
  if (!result || result.success !== true) {
    const errorBody = body as ApiErrorResponse | null;
    throw new ApiError(
      errorBody?.error || "The server returned an invalid response.",
      response.status,
      body,
    );
  }

  return result.data;
}

export async function predictCargo(payload: PredictRequest): Promise<PredictResponse> {
  const response = await fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<PredictResponse>(response);
}

export async function getCargo(): Promise<CargoRecord[]> {
  const response = await fetch("/cargo");
  return handleResponse<CargoRecord[]>(response);
}

export async function getCargoById(id: string): Promise<CargoRecord> {
  const response = await fetch(`/cargo/${encodeURIComponent(id)}`);
  return handleResponse<CargoRecord>(response);
}

export async function createCargo(cargo: CargoInput): Promise<CargoRecord> {
  const response = await fetch("/cargo", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cargo),
  });
  return handleResponse<CargoRecord>(response);
}

export async function updateCargo(id: string, cargo: CargoUpdateInput): Promise<CargoRecord> {
  const response = await fetch(`/cargo/${encodeURIComponent(id)}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cargo),
  });
  return handleResponse<CargoRecord>(response);
}

export async function deleteCargo(id: string): Promise<void> {
  const response = await fetch(`/cargo/${encodeURIComponent(id)}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    let body: unknown = null;
    try { body = await response.json(); } catch { body = await response.text().catch(() => null); }
    const errorBody = body as ApiErrorResponse | null;
    throw new ApiError(
      errorBody?.error || `Delete failed: ${response.status} ${response.statusText}`,
      response.status,
      body,
    );
  }
}

export { ApiError };
