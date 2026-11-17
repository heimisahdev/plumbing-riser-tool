import { NextRequest } from 'next/server';

export async function GET(_request: NextRequest, { params }: { params: { projectId: string } }) {
  const csv = [
    'fixture_id,fixture_name,quantity,unit,dfu',
    'WC,Water Closet,12,ea,48',
    'LAV,Lavatory,8,ea,8',
    'KS,Kitchen Sink,4,ea,8',
  ].join('\n');

  return new Response(csv, {
    headers: {
      'Content-Type': 'text/csv; charset=utf-8',
      'Content-Disposition': `attachment; filename="${params.projectId || 'project'}-takeoff.csv"`,
    },
  });
}
