// app/dashboard/page.tsx
import { ProtectedRoute } from '@/app/components/ProtectedRoute';

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <h2>Welcome to your dashboard</h2>
      {/* … */}
    </ProtectedRoute>
  );
}
