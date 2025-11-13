import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { stallsAPI } from '../../services/api';

interface Stall {
  id: number;
  name: string;
  location: string;
  cuisine_type: string;
  rating: number;
  is_open: boolean;
  image_url?: string;
  distance?: number;
}

interface StallsState {
  stalls: Stall[];
  selectedStall: Stall | null;
  loading: boolean;
  error: string | null;
}

const initialState: StallsState = {
  stalls: [],
  selectedStall: null,
  loading: false,
  error: null,
};

// Async thunks
export const fetchStalls = createAsyncThunk(
  'stalls/fetchAll',
  async (_, { rejectWithValue }) => {
    try {
      const response = await stallsAPI.getAll();
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch stalls');
    }
  }
);

export const fetchNearbyStalls = createAsyncThunk(
  'stalls/fetchNearby',
  async ({ lat, lng }: { lat: number; lng: number }, { rejectWithValue }) => {
    try {
      const response = await stallsAPI.getNearby(lat, lng);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch nearby stalls');
    }
  }
);

export const fetchStallById = createAsyncThunk(
  'stalls/fetchById',
  async (id: number, { rejectWithValue }) => {
    try {
      const response = await stallsAPI.getById(id);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch stall');
    }
  }
);

const stallsSlice = createSlice({
  name: 'stalls',
  initialState,
  reducers: {
    setSelectedStall: (state, action: PayloadAction<Stall | null>) => {
      state.selectedStall = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch all stalls
      .addCase(fetchStalls.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchStalls.fulfilled, (state, action) => {
        state.loading = false;
        state.stalls = action.payload;
      })
      .addCase(fetchStalls.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch nearby stalls
      .addCase(fetchNearbyStalls.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchNearbyStalls.fulfilled, (state, action) => {
        state.loading = false;
        state.stalls = action.payload;
      })
      .addCase(fetchNearbyStalls.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Fetch stall by ID
      .addCase(fetchStallById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchStallById.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedStall = action.payload;
      })
      .addCase(fetchStallById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setSelectedStall, clearError } = stallsSlice.actions;
export default stallsSlice.reducer;
