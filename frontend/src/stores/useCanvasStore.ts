import { create } from 'zustand';

type SelectionMode = 'PAN_ZOOM' | 'POINT_SELECT' | 'LASSO_SELECT' | 'ROOM_ZONE' | 'PLACE_RISER';

export const useCanvasStore = create<{
  currentMode: SelectionMode;
  activeRiserTag: string | null;
  setMode: (mode: SelectionMode) => void;
  setActiveRiserTag: (tag: string | null) => void;
}>((set) => ({
  currentMode: 'PAN_ZOOM',
  activeRiserTag: 'R-01',
  setMode: (mode) => set({ currentMode: mode }),
  setActiveRiserTag: (tag) => set({ activeRiserTag: tag }),
}));
