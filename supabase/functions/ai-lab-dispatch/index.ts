// Supabase Edge Function: ai-lab-dispatch
// Deploy only after configuring GITHUB_WORKFLOW_TOKEN in Supabase secrets.
// The token must have Actions: write on the single repository.
import { createClient } from 'npm:@supabase/supabase-js@2';

const owner = 'bogusbogucki95-stack';
const repo = 'ai-lab1';
const workflow = 'agent-report.yml';
Deno.serve(async (req) => {
  const origin = req.headers.get('origin') || '';
  const allowed = 'https://bogusbogucki95-stack.github.io';
  const cors = {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Headers': 'authorization, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Vary': 'Origin',
  };
  if (req.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
  if (origin !== allowed) return Response.json({ error: 'Origin not allowed' }, { status: 403, headers: cors });
  if (req.method !== 'POST') return Response.json({ error: 'Method not allowed' }, { status: 405, headers: cors });
  try {
    const auth = req.headers.get('Authorization') || '';
    if (!auth.startsWith('Bearer ')) return Response.json({ error: 'Login required' }, { status: 401, headers: cors });
    const supabase = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_ANON_KEY')!, { global: { headers: { Authorization: auth } } });
    const { data, error } = await supabase.auth.getUser();
    if (error || !data.user) return Response.json({ error: 'Invalid session' }, { status: 401, headers: cors });
    const input = await req.json();
    const task = typeof input.task === 'string' ? input.task.trim() : '';
    const category = input.category;
    if (!task || task.length > 500 || !['checklist', 'risk', 'ecommerce'].includes(category))
      return Response.json({ error: 'Invalid task or category' }, { status: 400, headers: cors });
    const token = Deno.env.get('GITHUB_WORKFLOW_TOKEN');
    if (!token) return Response.json({ error: 'Server token not configured' }, { status: 503, headers: cors });
    const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/actions/workflows/${workflow}/dispatches`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28', 'Content-Type': 'application/json' },
      body: JSON.stringify({ ref: 'main', inputs: { task, category } }),
    });
    if (!response.ok) return Response.json({ error: 'GitHub workflow dispatch failed', status: response.status }, { status: 502, headers: cors });
    return Response.json({ ok: true, message: 'Workflow queued; report available in GitHub Actions after completion.' }, { headers: cors });
  } catch {
    return Response.json({ error: 'Unexpected server error' }, { status: 500, headers: cors });
  }
});
