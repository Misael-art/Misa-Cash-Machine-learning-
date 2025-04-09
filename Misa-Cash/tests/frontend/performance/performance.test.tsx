import { test, expect } from '@playwright/test';
import { performance } from 'perf_hooks';

test.describe('Performance Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('First Contentful Paint (FCP)', async ({ page }) => {
    const fcp = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((entryList) => {
          const entries = entryList.getEntries();
          resolve(entries[0].startTime);
        }).observe({ entryTypes: ['paint'] });
      });
    });
    expect(fcp).toBeLessThan(1000); // FCP deve ser menor que 1 segundo
  });

  test('Largest Contentful Paint (LCP)', async ({ page }) => {
    const lcp = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((entryList) => {
          const entries = entryList.getEntries();
          resolve(entries[entries.length - 1].startTime);
        }).observe({ entryTypes: ['largest-contentful-paint'] });
      });
    });
    expect(lcp).toBeLessThan(2500); // LCP deve ser menor que 2.5 segundos
  });

  test('Time to Interactive (TTI)', async ({ page }) => {
    const tti = await page.evaluate(() => {
      return new Promise((resolve) => {
        let tti = 0;
        const observer = new PerformanceObserver((entryList) => {
          for (const entry of entryList.getEntries()) {
            if (entry.name === 'first-interactive') {
              tti = entry.startTime;
              observer.disconnect();
              resolve(tti);
            }
          }
        });
        observer.observe({ entryTypes: ['measure'] });
      });
    });
    expect(tti).toBeLessThan(3500); // TTI deve ser menor que 3.5 segundos
  });

  test('Cumulative Layout Shift (CLS)', async ({ page }) => {
    const cls = await page.evaluate(() => {
      return new Promise((resolve) => {
        let clsValue = 0;
        new PerformanceObserver((entryList) => {
          for (const entry of entryList.getEntries()) {
            if (!entry.hadRecentInput) {
              clsValue += entry.value;
            }
          }
          resolve(clsValue);
        }).observe({ entryTypes: ['layout-shift'] });
      });
    });
    expect(cls).toBeLessThan(0.1); // CLS deve ser menor que 0.1
  });

  test('First Input Delay (FID)', async ({ page }) => {
    const fid = await page.evaluate(() => {
      return new Promise((resolve) => {
        new PerformanceObserver((entryList) => {
          const entries = entryList.getEntries();
          resolve(entries[0].processingStart - entries[0].startTime);
        }).observe({ entryTypes: ['first-input'] });
      });
    });
    expect(fid).toBeLessThan(100); // FID deve ser menor que 100ms
  });

  test('Memory Usage', async ({ page }) => {
    const memory = await page.evaluate(() => {
      return performance.memory?.usedJSHeapSize / 1024 / 1024; // MB
    });
    expect(memory).toBeLessThan(50); // Uso de memória deve ser menor que 50MB
  });

  test('Network Requests', async ({ page }) => {
    const requests = await page.evaluate(() => {
      return performance.getEntriesByType('resource').length;
    });
    expect(requests).toBeLessThan(50); // Número de requisições deve ser menor que 50
  });
}); 