export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api";

export type UploadResponse = {
  document_id: string;
  filename: string;
};

export async function getApiHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`, {
    method: "GET",
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Health request failed with status ${response.status}`);
  }

  return (await response.json()) as { status: string };
}

export async function uploadPdf(file: File): Promise<UploadResponse> {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${API_BASE_URL}/documents/upload`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    throw new Error(`Upload failed with status ${response.status}`);
  }

  return (await response.json()) as UploadResponse;
}
