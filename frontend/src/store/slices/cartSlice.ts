import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CartItem {
  menu_item_id: number;
  name: string;
  price: number;
  quantity: number;
  special_requests?: string;
  stall_id: number;
  stall_name: string;
}

interface CartState {
  items: CartItem[];
  stallId: number | null;
  stallName: string | null;
  total: number;
  itemCount: number;
}

const initialState: CartState = {
  items: [],
  stallId: null,
  stallName: null,
  total: 0,
  itemCount: 0,
};

// Helper function to calculate totals
const calculateTotals = (items: CartItem[]) => {
  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const itemCount = items.reduce((count, item) => count + item.quantity, 0);
  return { total, itemCount };
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    addToCart: (state, action: PayloadAction<CartItem>) => {
      const item = action.payload;

      // Check if adding from different stall
      if (state.stallId && state.stallId !== item.stall_id) {
        // This should be handled in the component with a confirmation dialog
        return;
      }

      // Set stall info if first item
      if (!state.stallId) {
        state.stallId = item.stall_id;
        state.stallName = item.stall_name;
      }

      // Check if item already exists in cart
      const existingItem = state.items.find(
        (i) => i.menu_item_id === item.menu_item_id
      );

      if (existingItem) {
        existingItem.quantity += item.quantity;
      } else {
        state.items.push(item);
      }

      // Recalculate totals
      const { total, itemCount } = calculateTotals(state.items);
      state.total = total;
      state.itemCount = itemCount;
    },
    removeFromCart: (state, action: PayloadAction<number>) => {
      state.items = state.items.filter(
        (item) => item.menu_item_id !== action.payload
      );

      // Clear stall info if cart is empty
      if (state.items.length === 0) {
        state.stallId = null;
        state.stallName = null;
      }

      // Recalculate totals
      const { total, itemCount } = calculateTotals(state.items);
      state.total = total;
      state.itemCount = itemCount;
    },
    updateQuantity: (
      state,
      action: PayloadAction<{ menu_item_id: number; quantity: number }>
    ) => {
      const { menu_item_id, quantity } = action.payload;
      const item = state.items.find((i) => i.menu_item_id === menu_item_id);

      if (item) {
        if (quantity <= 0) {
          state.items = state.items.filter((i) => i.menu_item_id !== menu_item_id);
        } else {
          item.quantity = quantity;
        }

        // Clear stall info if cart is empty
        if (state.items.length === 0) {
          state.stallId = null;
          state.stallName = null;
        }

        // Recalculate totals
        const { total, itemCount } = calculateTotals(state.items);
        state.total = total;
        state.itemCount = itemCount;
      }
    },
    updateSpecialRequests: (
      state,
      action: PayloadAction<{ menu_item_id: number; special_requests: string }>
    ) => {
      const { menu_item_id, special_requests } = action.payload;
      const item = state.items.find((i) => i.menu_item_id === menu_item_id);

      if (item) {
        item.special_requests = special_requests;
      }
    },
    clearCart: (state) => {
      state.items = [];
      state.stallId = null;
      state.stallName = null;
      state.total = 0;
      state.itemCount = 0;
    },
    loadCartFromStorage: (state, action: PayloadAction<CartState>) => {
      return action.payload;
    },
  },
});

export const {
  addToCart,
  removeFromCart,
  updateQuantity,
  updateSpecialRequests,
  clearCart,
  loadCartFromStorage,
} = cartSlice.actions;

export default cartSlice.reducer;
