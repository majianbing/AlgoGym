export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type Stats = {
  current_streak: number;
  longest_streak: number;
  total_sessions: number;
  solved_sessions: number;
  documents: number;
};

export type Problem = {
  id: number;
  title: string;
  pattern: string;
  difficulty: string;
  day?: number;
  prompt: string;
};

export type PracticeSession = {
  id: number;
  date: string;
  problem_id: number;
  status: string;
  time_spent_mins: number;
  notes: string;
  hint_level_used: number;
  review_due: string | null;
  problem?: Problem;
};

export type Today = {
  date: string;
  problem: Problem | null;
  workout: Record<string, string>;
  session: PracticeSession | null;
};

export type DocumentRecord = {
  id: number;
  filename: string;
  chunked: boolean;
  embedded: boolean;
  chunks_count: number;
  created_at: string;
};

export type PlanWeek = {
  week: number;
  problems: Array<Problem & { day: number; leetcode_url: string }>;
};

export type ReviewData = {
  due_sessions: PracticeSession[];
  weak_patterns: Array<{ pattern: string; failures: number; is_weak: boolean }>;
};

export type RuntimeSettings = {
  runtime: {
    ollama_base_url: string;
    llm_model: string;
    embedding_model: string;
    chroma_path: string;
  };
  preferences: Record<string, string>;
};

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers:
      init?.body instanceof FormData
        ? init.headers
        : { "Content-Type": "application/json", ...init?.headers },
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? `Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}
