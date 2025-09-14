"""
Cache utility functions for subject app
"""
from django.core.cache import cache
from django.conf import settings
import json
import hashlib


class SubjectCache:
    """Subject app cache management class"""
    
    # Cache timeout constants (in seconds)
    CACHE_TIMEOUT_SHORT = 5 * 60        # 5 minutes
    CACHE_TIMEOUT_MEDIUM = 15 * 60      # 15 minutes  
    CACHE_TIMEOUT_LONG = 60 * 60        # 1 hour
    
    # Cache key templates
    MARHALA_LIST_KEY = "wems:marhala:list"
    MARHALA_DETAIL_KEY = "wems:marhala:detail:{id}"
    MARHALA_WITH_COUNTS_KEY = "wems:marhala:with_counts"
    MARHALA_SUBJECTS_KEY = "wems:marhala:{id}:subjects"
    
    SUBJECT_LIST_KEY = "wems:subject:list"
    SUBJECT_DETAIL_KEY = "wems:subject:detail:{id}"
    SUBJECT_BY_MARHALA_KEY = "wems:subject:marhala:{marhala_id}"
    
    SUBJECT_SETTINGS_LIST_KEY = "wems:subject_settings:list"
    SUBJECT_SETTINGS_DETAIL_KEY = "wems:subject_settings:detail:{id}"
    SUBJECT_SETTING_DETAIL_KEY = "wems:subject_settings:detail:{id}"
    SUBJECT_SETTINGS_BY_MARHALA_KEY = "wems:subject_settings:marhala:{marhala_id}"
    
    @staticmethod
    def generate_key_with_params(key_template, **params):
        """Generate cache key with parameters"""
        return key_template.format(**params)
    
    @staticmethod
    def generate_query_key(base_key, query_params=None):
        """Generate cache key for queries with parameters"""
        if query_params:
            # Sort parameters for consistent key generation
            sorted_params = sorted(query_params.items())
            params_str = json.dumps(sorted_params, sort_keys=True)
            params_hash = hashlib.md5(params_str.encode()).hexdigest()[:8]
            return f"{base_key}:query:{params_hash}"
        return base_key
    
    @staticmethod
    def set_cache(key, data, timeout=None):
        """Set cache with default timeout"""
        if timeout is None:
            timeout = SubjectCache.CACHE_TIMEOUT_MEDIUM
        return cache.set(key, data, timeout)
    
    @staticmethod
    def get_cache(key):
        """Get cache data"""
        return cache.get(key)
    
    @staticmethod
    def delete_cache(key):
        """Delete cache data"""
        return cache.delete(key)
    
    @staticmethod
    def delete_pattern(pattern):
        """Delete cache keys matching pattern"""
        try:
            # For locmem cache, keys() method might not be available
            # So we'll just clear the entire cache for safety
            if hasattr(cache, '_cache') and hasattr(cache._cache, 'keys'):
                # Try to get keys matching pattern
                all_keys = list(cache._cache.keys())
                matching_keys = [key for key in all_keys if pattern in str(key)]
                if matching_keys:
                    cache.delete_many(matching_keys)
                    return len(matching_keys)
            else:
                # Fallback: clear entire cache
                cache.clear()
                return 1
            return 0
        except Exception as e:
            print(f"Error deleting pattern {pattern}: {e}")
            # Fallback: clear entire cache
            try:
                cache.clear()
                return 1
            except:
                return 0
    
    @staticmethod
    def invalidate_pattern_cache(pattern):
        """Invalidate cache keys matching pattern - alias for delete_pattern"""
        return SubjectCache.delete_pattern(pattern)
    
    @classmethod
    def invalidate_marhala_cache(cls, marhala_id=None):
        """Invalidate marhala related cache"""
        # Delete general marhala caches
        cls.delete_cache(cls.MARHALA_LIST_KEY)
        cls.delete_cache(cls.MARHALA_WITH_COUNTS_KEY)
        
        if marhala_id:
            # Delete specific marhala cache
            cls.delete_cache(cls.generate_key_with_params(cls.MARHALA_DETAIL_KEY, id=marhala_id))
            cls.delete_cache(cls.generate_key_with_params(cls.MARHALA_SUBJECTS_KEY, id=marhala_id))
            cls.delete_cache(cls.generate_key_with_params(cls.SUBJECT_BY_MARHALA_KEY, marhala_id=marhala_id))
            cls.delete_cache(cls.generate_key_with_params(cls.SUBJECT_SETTINGS_BY_MARHALA_KEY, marhala_id=marhala_id))
    
    @classmethod
    def invalidate_subject_cache(cls, subject_id=None, marhala_id=None):
        """Invalidate subject related cache"""
        # Delete general subject caches
        cls.delete_cache(cls.SUBJECT_LIST_KEY)
        
        if subject_id:
            cls.delete_cache(cls.generate_key_with_params(cls.SUBJECT_DETAIL_KEY, id=subject_id))
        
        if marhala_id:
            cls.delete_cache(cls.generate_key_with_params(cls.SUBJECT_BY_MARHALA_KEY, marhala_id=marhala_id))
            cls.delete_cache(cls.generate_key_with_params(cls.MARHALA_SUBJECTS_KEY, id=marhala_id))
    
    @classmethod
    def invalidate_subject_settings_cache(cls, settings_id=None, marhala_id=None):
        """Invalidate subject settings related cache"""
        # Delete general subject settings caches
        cls.delete_cache(cls.SUBJECT_SETTINGS_LIST_KEY)
        
        if settings_id:
            cls.delete_cache(cls.generate_key_with_params(cls.SUBJECT_SETTINGS_DETAIL_KEY, id=settings_id))
        
        if marhala_id:
            cls.delete_cache(cls.generate_key_with_params(cls.SUBJECT_SETTINGS_BY_MARHALA_KEY, marhala_id=marhala_id))
    
    @classmethod
    def invalidate_all_cache(cls):
        """Invalidate all subject app related cache"""
        cls.delete_pattern("wems:marhala")
        cls.delete_pattern("wems:subject")