export async function GET() {
  return Response.json({
    tag: 'R-01',
    total_stack_dfu: 26,
    floors: [
      { floor: 11, fixtures: ['WC', 'LAV'], floor_dfu: 5.5, cumulative_dfu: 26 },
      { floor: 9, fixtures: ['WC', 'KS'], floor_dfu: 8.0, cumulative_dfu: 20.5 },
      { floor: 7, fixtures: ['LAV'], floor_dfu: 1.0, cumulative_dfu: 12.5 },
      { floor: 5, fixtures: ['WC'], floor_dfu: 4.0, cumulative_dfu: 11.5 },
    ],
    offsets: [
      {
        lower_sheet: 'A-103.00',
        upper_sheet: 'A-104.00',
        transition_floor: 11,
        horizontal_displacement_feet: 5.4,
        developed_pipe_length_feet: 7.64,
      },
    ],
  });
}
