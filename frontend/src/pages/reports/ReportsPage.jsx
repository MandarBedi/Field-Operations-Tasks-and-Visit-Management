import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { reportsAPI } from '../../api'

function Table({ cols, rows = [] }) {
  if (!rows.length) return <p style={{ color: '#888', fontSize: 13 }}>No data.</p>
  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: 8, fontSize: 13 }}>
        <thead><tr style={{ background: '#f0f2f5' }}>{cols.map(c => <th key={c} style={{ padding: '10px 12px', textAlign: 'left', whiteSpace: 'nowrap' }}>{c}</th>)}</tr></thead>
        <tbody>{rows.map((row, i) => <tr key={i} style={{ borderBottom: '1px solid #f0f0f0' }}>{row.map((cell, j) => <td key={j} style={{ padding: '9px 12px' }}>{cell}</td>)}</tr>)}</tbody>
      </table>
    </div>
  )
}

export default function ReportsPage() {
  const [days, setDays] = useState(30)

  const { data: ts, isLoading: l1 } = useQuery({ queryKey: ['rpt-task', days], queryFn: () => reportsAPI.taskSummary({ days }).then(r => r.data) })
  const { data: ap, isLoading: l2 } = useQuery({ queryKey: ['rpt-agent'], queryFn: () => reportsAPI.agentPerformance().then(r => r.data) })
  const { data: vo, isLoading: l3 } = useQuery({ queryKey: ['rpt-visit', days], queryFn: () => reportsAPI.visitOutcomes({ days }).then(r => r.data) })

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Reports</h2>
        <select value={days} onChange={e => setDays(Number(e.target.value))} style={{ padding: '7px 10px', border: '1px solid #ddd', borderRadius: 4 }}>
          {[7, 14, 30, 60, 90].map(d => <option key={d} value={d}>Last {d} days</option>)}
        </select>
      </div>

      <div style={{ marginBottom: 32 }}>
        <h4>Task Summary by Region / Priority / Status</h4>
        {l1 ? <p>Loading...</p> : <Table cols={['Region', 'Priority', 'Status', 'Tasks', 'Overdue']} rows={ts?.rows?.map(r => [r.region, r.priority, r.status, r.task_count, r.overdue_count])} />}
      </div>

      <div style={{ marginBottom: 32 }}>
        <h4>Agent Performance</h4>
        {l2 ? <p>Loading...</p> : <Table
          cols={['Agent', 'Team', 'Region', 'Tasks Assigned', 'Completed', 'Task %', 'Visits', 'Successful', 'Success %', 'Avg Min']}
          rows={ap?.rows?.map(r => [r.username, r.team ?? '—', r.region ?? '—', r.total_tasks_assigned, r.tasks_completed, r.task_completion_pct ?? '—', r.total_visits, r.successful_visits, r.visit_success_pct ?? '—', r.avg_visit_duration_min ?? '—'])}
        />}
      </div>

      <div style={{ marginBottom: 32 }}>
        <h4>Visit Outcomes by Week</h4>
        {l3 ? <p>Loading...</p> : <Table
          cols={['Week', 'Outcome', 'Visits', 'Avg Duration (min)', '% of Week']}
          rows={vo?.rows?.map(r => [r.week_start, r.outcome, r.visit_count, r.avg_duration_min ?? '—', r.pct_of_week ?? '—'])}
        />}
      </div>
    </div>
  )
}
