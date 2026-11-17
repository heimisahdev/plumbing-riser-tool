export async function POST(request: Request) {
  const payload = await request.json();
  const polygon = Array.isArray(payload.polygon) ? payload.polygon : [];
  const assignedRiser = payload.assigned_riser_tag || 'R-01';

  return Response.json(
    polygon.slice(0, 8).map((point: any, index: number) => ({
      id: `pop-${index + 1}`,
      riser: assignedRiser,
      x: Number(point?.x ?? 0),
      y: Number(point?.y ?? 0),
    })),
  );
}
