import { useReducer, useEffect } from 'react'
import { CartContext } from './CartContextDefinition'
import { makeCartItemId } from '../utils/cartUtils'

const STORAGE_KEY = 'driftwood_cart'
const TTL_MS = 24 * 60 * 60 * 1000 // 24 hours

const cartReducer = (state, action) => {
    switch (action.type) {
        case 'ADD_ITEM': {
            // cartItemId is the line-item identity; id is the product catalogue id
            const { cartItemId } = action.payload
            const existingItem = state.items.find(item => item.cartItemId === cartItemId)
            if (existingItem) {
                return {
                    ...state,
                    items: state.items.map(item =>
                        item.cartItemId === cartItemId
                            ? { ...item, quantity: item.quantity + 1 }
                            : item
                    ),
                    totalItems: state.totalItems + 1
                }
            }
            return {
                ...state,
                items: [...state.items, { ...action.payload, quantity: 1 }],
                totalItems: state.totalItems + 1
            }
        }

        case 'REMOVE_ITEM': {
            // payload is cartItemId
            const itemToRemove = state.items.find(item => item.cartItemId === action.payload)
            if (!itemToRemove) return state
            if (itemToRemove.quantity === 1) {
                return {
                    ...state,
                    items: state.items.filter(item => item.cartItemId !== action.payload),
                    totalItems: state.totalItems - 1
                }
            }
            return {
                ...state,
                items: state.items.map(item =>
                    item.cartItemId === action.payload
                        ? { ...item, quantity: item.quantity - 1 }
                        : item
                ),
                totalItems: state.totalItems - 1
            }
        }

        case 'REMOVE_ENTIRE_ITEM': {
            // payload is cartItemId
            const itemToRemove = state.items.find(item => item.cartItemId === action.payload)
            if (!itemToRemove) return state
            return {
                ...state,
                items: state.items.filter(item => item.cartItemId !== action.payload),
                totalItems: state.totalItems - itemToRemove.quantity
            }
        }

        case 'CLEAR_CART':
            return { items: [], totalItems: 0 }

        default:
            return state
    }
}

const emptyState = { items: [], totalItems: 0 }

function loadFromStorage() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY)
        if (!raw) return emptyState

        const { state, savedAt } = JSON.parse(raw)

        // Discard if older than 24 hours
        if (Date.now() - savedAt > TTL_MS) {
            localStorage.removeItem(STORAGE_KEY)
            return emptyState
        }

        // Discard if any item still has a legacy dollar price (e.g. "$3.50")
        // This clears the cart once after the currency migration so users
        // don't see stale $ amounts in the cart UI.
        const hasLegacyPrices = state.items?.some(item =>
            String(item.price).trim().startsWith('$')
        )
        if (hasLegacyPrices) {
            localStorage.removeItem(STORAGE_KEY)
            return emptyState
        }

        return state
    } catch {
        return emptyState
    }
}

function saveToStorage(state) {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ state, savedAt: Date.now() }))
    } catch {
        // storage unavailable — fail silently
    }
}

export const CartProvider = ({ children }) => {
    const [state, dispatch] = useReducer(cartReducer, undefined, loadFromStorage)

    // Sync to localStorage on every cart change
    useEffect(() => {
        saveToStorage(state)
    }, [state])

    const addToCart = (item) => dispatch({
        type: 'ADD_ITEM',
        payload: {
            ...item,
            cartItemId: makeCartItemId(item.id, item.customizations),
        }
    })
    const removeFromCart = (cartItemId) => dispatch({ type: 'REMOVE_ITEM', payload: cartItemId })
    const removeEntireItem = (cartItemId) => dispatch({ type: 'REMOVE_ENTIRE_ITEM', payload: cartItemId })
    const clearCart = () => dispatch({ type: 'CLEAR_CART' })

    return (
        <CartContext.Provider value={{
            ...state,
            addToCart,
            removeFromCart,
            removeEntireItem,
            clearCart
        }}>
            {children}
        </CartContext.Provider>
    )
}
