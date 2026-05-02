# Frontend — React, Next.js, TypeScript

Carregue quando a tarefa envolver componentes React, Next.js App Router, hooks, state management ou integração com APIs.

---

## Estrutura Next.js (App Router)

```
src/
├── app/
│   ├── layout.tsx           # root layout
│   ├── page.tsx             # home
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   └── dashboard/
│       ├── layout.tsx       # dashboard layout
│       └── page.tsx
├── components/
│   ├── ui/                  # Button, Input, Modal (shadcn ou custom)
│   └── features/            # UserCard, OrderList
├── lib/
│   ├── api.ts               # cliente axios/fetch configurado
│   ├── auth.ts
│   └── utils.ts
├── hooks/
│   ├── useAuth.ts
│   └── useDebounce.ts
├── types/
│   └── index.ts
└── styles/
    └── globals.css
```

---

## React Query — Server State

```typescript
// lib/api.ts
import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  withCredentials: true,
});

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error.response?.status === 401) {
      // refresh token ou redirect
    }
    return Promise.reject(error);
  }
);

// hooks/useUsers.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';

export const useUsers = () =>
  useQuery({
    queryKey: ['users'],
    queryFn: () => api.get('/users').then((r) => r.data),
    staleTime: 1000 * 60 * 5,  // 5 min
  });

export const useCreateUser = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UserCreate) => api.post('/users', data).then((r) => r.data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
  });
};
```

---

## Componente com Form e Validação

```typescript
'use client';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useCreateUser } from '@/hooks/useUsers';

const schema = z.object({
  name: z.string().min(2, 'Name too short'),
  email: z.string().email('Invalid email'),
});

type FormData = z.infer<typeof schema>;

export function CreateUserForm() {
  const { mutate, isPending, error } = useCreateUser();
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
  });

  return (
    <form onSubmit={handleSubmit((data) => mutate(data))} className="space-y-4">
      <div>
        <input {...register('name')} placeholder="Name" className="input" />
        {errors.name && <p className="text-red-500 text-sm">{errors.name.message}</p>}
      </div>
      <div>
        <input {...register('email')} placeholder="Email" className="input" />
        {errors.email && <p className="text-red-500 text-sm">{errors.email.message}</p>}
      </div>
      {error && <p className="text-red-500">Failed to create user</p>}
      <button type="submit" disabled={isPending} className="btn btn-primary">
        {isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

---

## Server Components + Data Fetching

```typescript
// app/dashboard/page.tsx — Server Component (sem 'use client')
import { Suspense } from 'react';
import { UserList } from '@/components/features/UserList';

export default async function DashboardPage() {
  const users = await fetch(`${process.env.API_URL}/users`, {
    next: { revalidate: 60 },  // ISR: revalida a cada 60s
  }).then((r) => r.json());

  return (
    <main>
      <h1>Dashboard</h1>
      <Suspense fallback={<div>Loading...</div>}>
        <UserList initialData={users} />
      </Suspense>
    </main>
  );
}
```

---

## Custom Hooks

```typescript
// hooks/useDebounce.ts
import { useState, useEffect } from 'react';

export function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debounced;
}

// hooks/useLocalStorage.ts
import { useState, useCallback } from 'react';

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setItem = useCallback((newValue: T) => {
    setValue(newValue);
    localStorage.setItem(key, JSON.stringify(newValue));
  }, [key]);

  return [value, setItem] as const;
}
```

---

## Dependências Frontend

```json
{
  "dependencies": {
    "next": "^14.2",
    "react": "^18.3",
    "react-dom": "^18.3",
    "@tanstack/react-query": "^5.40",
    "axios": "^1.7",
    "react-hook-form": "^7.51",
    "@hookform/resolvers": "^3.6",
    "zod": "^3.23",
    "zustand": "^4.5",
    "clsx": "^2.1",
    "tailwind-merge": "^2.3"
  },
  "devDependencies": {
    "typescript": "^5.4",
    "@types/react": "^18.3",
    "@types/node": "^20",
    "tailwindcss": "^3.4",
    "eslint": "^8",
    "prettier": "^3"
  }
}
```
