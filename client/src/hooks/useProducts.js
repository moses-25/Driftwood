import { useState, useEffect } from 'react';
import { getProducts, getCategories } from '../services/api';
import { transformProducts, transformCategory } from '../utils/dataTransformers';

/**
 * Custom hook to fetch and manage products from the backend
 */
export const useProducts = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch products and categories in parallel
        const [productsResponse, categoriesResponse] = await Promise.all([
          getProducts({ per_page: 100, is_available: true }),
          getCategories(),
        ]);

        // Transform backend data to frontend format
        const transformedProducts = transformProducts(productsResponse.data || []);
        const transformedCategories = (categoriesResponse.data || [])
          .filter(cat => cat.is_active)
          .map(transformCategory);

        setProducts(transformedProducts);
        setCategories(transformedCategories);
      } catch (err) {
        console.error('Error fetching products:', err);
        setError(err.message || 'Failed to load products');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { products, categories, loading, error };
};

/**
 * Custom hook to fetch products by category
 */
export const useProductsByCategory = (categoryId) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!categoryId) {
      setProducts([]);
      setLoading(false);
      return;
    }

    const fetchProducts = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await getProducts({ 
          category_id: categoryId, 
          is_available: true,
          per_page: 100 
        });

        const transformedProducts = transformProducts(response.data || []);
        setProducts(transformedProducts);
      } catch (err) {
        console.error('Error fetching products by category:', err);
        setError(err.message || 'Failed to load products');
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [categoryId]);

  return { products, loading, error };
};
