package androidx.appcompat.app;

import android.content.res.Resources;
import android.os.Build.VERSION;
import android.util.Log;
import android.util.LongSparseArray;
import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import java.lang.reflect.Field;
import java.util.Map;

class ResourcesFlusher {
    private static final String TAG = "ResourcesFlusher";
    private static Field sDrawableCacheField;
    private static boolean sDrawableCacheFieldFetched;
    private static Field sResourcesImplField;
    private static boolean sResourcesImplFieldFetched;
    private static Class sThemedResourceCacheClazz;
    private static boolean sThemedResourceCacheClazzFetched;
    private static Field sThemedResourceCache_mUnthemedEntriesField;
    private static boolean sThemedResourceCache_mUnthemedEntriesFieldFetched;

    static void flush(@NonNull Resources resources) {
        if (VERSION.SDK_INT < 28) {
            if (VERSION.SDK_INT >= 24) {
                flushNougats(resources);
            } else if (VERSION.SDK_INT >= 23) {
                flushMarshmallows(resources);
            } else if (VERSION.SDK_INT >= 21) {
                flushLollipops(resources);
            }
        }
    }

    @RequiresApi(21)
    private static void flushLollipops(@NonNull Resources resources) {
        boolean z = sDrawableCacheFieldFetched;
        String str = TAG;
        if (!z) {
            try {
                sDrawableCacheField = Resources.class.getDeclaredField("mDrawableCache");
                sDrawableCacheField.setAccessible(true);
            } catch (NoSuchFieldException e) {
                Log.e(str, "Could not retrieve Resources#mDrawableCache field", e);
            }
            sDrawableCacheFieldFetched = true;
        }
        Field field = sDrawableCacheField;
        if (field != null) {
            Map drawableCache = null;
            try {
                drawableCache = (Map) field.get(resources);
            } catch (IllegalAccessException e2) {
                Log.e(str, "Could not retrieve value from Resources#mDrawableCache", e2);
            }
            if (drawableCache != null) {
                drawableCache.clear();
            }
        }
    }

    @RequiresApi(23)
    private static void flushMarshmallows(@NonNull Resources resources) {
        boolean z = sDrawableCacheFieldFetched;
        String str = TAG;
        if (!z) {
            try {
                sDrawableCacheField = Resources.class.getDeclaredField("mDrawableCache");
                sDrawableCacheField.setAccessible(true);
            } catch (NoSuchFieldException e) {
                Log.e(str, "Could not retrieve Resources#mDrawableCache field", e);
            }
            sDrawableCacheFieldFetched = true;
        }
        Object drawableCache = null;
        Field field = sDrawableCacheField;
        if (field != null) {
            try {
                drawableCache = field.get(resources);
            } catch (IllegalAccessException e2) {
                Log.e(str, "Could not retrieve value from Resources#mDrawableCache", e2);
            }
        }
        if (drawableCache != null) {
            flushThemedResourcesCache(drawableCache);
        }
    }

    @RequiresApi(24)
    private static void flushNougats(@NonNull Resources resources) {
        boolean z = sResourcesImplFieldFetched;
        String str = TAG;
        if (!z) {
            try {
                sResourcesImplField = Resources.class.getDeclaredField("mResourcesImpl");
                sResourcesImplField.setAccessible(true);
            } catch (NoSuchFieldException e) {
                Log.e(str, "Could not retrieve Resources#mResourcesImpl field", e);
            }
            sResourcesImplFieldFetched = true;
        }
        Field field = sResourcesImplField;
        if (field != null) {
            Object resourcesImpl = null;
            try {
                resourcesImpl = field.get(resources);
            } catch (IllegalAccessException e2) {
                Log.e(str, "Could not retrieve value from Resources#mResourcesImpl", e2);
            }
            if (resourcesImpl != null) {
                if (!sDrawableCacheFieldFetched) {
                    try {
                        sDrawableCacheField = resourcesImpl.getClass().getDeclaredField("mDrawableCache");
                        sDrawableCacheField.setAccessible(true);
                    } catch (NoSuchFieldException e3) {
                        Log.e(str, "Could not retrieve ResourcesImpl#mDrawableCache field", e3);
                    }
                    sDrawableCacheFieldFetched = true;
                }
                Object drawableCache = null;
                Field field2 = sDrawableCacheField;
                if (field2 != null) {
                    try {
                        drawableCache = field2.get(resourcesImpl);
                    } catch (IllegalAccessException e4) {
                        Log.e(str, "Could not retrieve value from ResourcesImpl#mDrawableCache", e4);
                    }
                }
                if (drawableCache != null) {
                    flushThemedResourcesCache(drawableCache);
                }
            }
        }
    }

    @RequiresApi(16)
    private static void flushThemedResourcesCache(@NonNull Object cache) {
        boolean z = sThemedResourceCacheClazzFetched;
        String str = TAG;
        if (!z) {
            try {
                sThemedResourceCacheClazz = Class.forName("android.content.res.ThemedResourceCache");
            } catch (ClassNotFoundException e) {
                Log.e(str, "Could not find ThemedResourceCache class", e);
            }
            sThemedResourceCacheClazzFetched = true;
        }
        Class cls = sThemedResourceCacheClazz;
        if (cls != null) {
            if (!sThemedResourceCache_mUnthemedEntriesFieldFetched) {
                try {
                    sThemedResourceCache_mUnthemedEntriesField = cls.getDeclaredField("mUnthemedEntries");
                    sThemedResourceCache_mUnthemedEntriesField.setAccessible(true);
                } catch (NoSuchFieldException ee) {
                    Log.e(str, "Could not retrieve ThemedResourceCache#mUnthemedEntries field", ee);
                }
                sThemedResourceCache_mUnthemedEntriesFieldFetched = true;
            }
            Field field = sThemedResourceCache_mUnthemedEntriesField;
            if (field != null) {
                LongSparseArray unthemedEntries = null;
                try {
                    unthemedEntries = (LongSparseArray) field.get(cache);
                } catch (IllegalAccessException e2) {
                    Log.e(str, "Could not retrieve value from ThemedResourceCache#mUnthemedEntries", e2);
                }
                if (unthemedEntries != null) {
                    unthemedEntries.clear();
                }
            }
        }
    }

    private ResourcesFlusher() {
    }
}
