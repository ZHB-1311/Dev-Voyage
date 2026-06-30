<!-- frontend/app/components/SkeletonCard.vue -->
<template>
  <div class="skeleton-card">
    <div class="skeleton-image"></div>
    <div class="skeleton-content">
      <div class="skeleton-title"></div>
      <div class="skeleton-text"></div>
      <div class="skeleton-text short"></div>
    </div>
  </div>
</template>

<style scoped>
.skeleton-card {
  background: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.skeleton-image {
  height: 200px;
  background: linear-gradient(
    90deg,
    var(--color-bg-tertiary) 25%,
    var(--color-bg-secondary) 50%,
    var(--color-bg-tertiary) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-content {
  padding: var(--space-4);
}

.skeleton-title,
.skeleton-text {
  height: 1rem;
  border-radius: var(--radius-sm);
  background: linear-gradient(
    90deg,
    var(--color-bg-tertiary) 25%,
    var(--color-bg-secondary) 50%,
    var(--color-bg-tertiary) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-title {
  width: 70%;
  height: 1.5rem;
  margin-bottom: var(--space-3);
}

.skeleton-text {
  margin-bottom: var(--space-2);
}

.skeleton-text.short {
  width: 50%;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>