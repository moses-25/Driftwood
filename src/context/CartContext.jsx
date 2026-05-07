import { useReducer } from 'react'
import { CartContext } from './CartContextDefinition'

const cartReducer = (state, action) => {
    switch (action.type) {
        case 'ADD_ITEM': {
            const existingItem = state.items.find(item => item.id === action.payload.id)

            if (existingItem) {
                return {
                    ...state,
                    items: state.items.map(item =>
                        item.id === action.payload.id
                            ? { ...item, quantity: item.quantity + 1 }
                            : item
                    ),
                    totalItems: state.totalItems + 1
                }
            } else {
                return {
                    ...state,
                    items: [...state.items, { ...action.payload, quantity: 1 }],
                    totalItems: state.totalItems + 1
                }
            }
        }

        case 'REMOVE_ITEM': {
            const itemToRemove = state.items.find(item => item.id === action.payload)

            if (!itemToRemove) return state

            if (itemToRemove.quantity === 1) {
                return {
                    ...state,
                    items: state.items.filter(item => item.id !== action.payload),
                    totalItems: state.totalItems - 1
                }
            } else {
                return {
                    ...state,
                    items: state.items.map(item =>
                        item.id === action.payload
                            ? { ...item, quantity: item.quantity - 1 }
                            : item
                    ),
                    totalItems: state.totalItems - 1
                }
            }
        }

        case 'REMOVE_ENTIRE_ITEM': {
            const itemToRemove = state.items.find(item => item.id === action.payload)

            if (!itemToRemove) return state

            return {
                ...state,
                items: state.items.filter(item => item.id !== action.payload),
                totalItems: state.totalItems - itemToRemove.quantity
            }
        }

        case 'CLEAR_CART':
            return {
                items: [],
                totalItems: 0
            }

        default:
            return state
    }
}

const initialState = {
    items: [],
    totalItems: 0
}

export const CartProvider = ({ children }) => {
    const [state, dispatch] = useReducer(cartReducer, initialState)

    const addToCart = (item) => {
        dispatch({ type: 'ADD_ITEM', payload: item })
    }

    const removeFromCart = (itemId) => {
        dispatch({ type: 'REMOVE_ITEM', payload: itemId })
    }

    const removeEntireItem = (itemId) => {
        dispatch({ type: 'REMOVE_ENTIRE_ITEM', payload: itemId })
    }

    const clearCart = () => {
        dispatch({ type: 'CLEAR_CART' })
    }

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