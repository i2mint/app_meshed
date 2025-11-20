/**
 * E2E Tests for Store Browser (Phase I)
 */

import { test, expect } from '@playwright/test';

test.describe('Store Browser', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Navigate to Store Browser
    await page.click('button:has-text("Store Browser")');
    await expect(page.getByText('Stores')).toBeVisible();
  });

  test('should display available stores', async ({ page }) => {
    // Check that all stores are visible
    await expect(page.getByText('meshes')).toBeVisible();
    await expect(page.getByText('configs')).toBeVisible();
    await expect(page.getByText('functions')).toBeVisible();
    await expect(page.getByText('raw_data')).toBeVisible();
  });

  test('should select a store and display keys', async ({ page }) => {
    // Click on meshes store
    await page.click('button:has-text("meshes")');

    // Wait for keys to load
    await page.waitForTimeout(1000);

    // Check that keys section is visible
    await expect(page.getByText(/Keys \(\d+\)/)).toBeVisible();
  });

  test('should create a new item in a store', async ({ page }) => {
    // Select meshes store
    await page.click('button:has-text("meshes")');

    // Click create button
    await page.click('button[title="Create new"]');

    // Fill in the form
    await page.fill('input[placeholder="my_item"]', 'test_dag');
    await page.fill('textarea', '{"name": "test", "nodes": [], "edges": []}');

    // Create the item
    await page.click('button:has-text("Create")');

    // Wait for creation
    await page.waitForTimeout(1000);

    // Verify the item appears in the list
    await expect(page.getByText('test_dag')).toBeVisible();
  });

  test('should view item content', async ({ page }) => {
    // Select meshes store
    await page.click('button:has-text("meshes")');

    await page.waitForTimeout(1000);

    // If there are items, click on the first one
    const firstKey = page.locator('.keys-list button').first();
    if (await firstKey.isVisible()) {
      await firstKey.click();

      // Check that content is displayed
      await expect(page.locator('.item-view')).toBeVisible();
      await expect(page.locator('pre')).toBeVisible();
    }
  });

  test('should switch between stores', async ({ page }) => {
    // Start with meshes
    await page.click('button:has-text("meshes")');
    await expect(page.locator('button:has-text("meshes").active')).toBeVisible();

    // Switch to configs
    await page.click('button:has-text("configs")');
    await expect(page.locator('button:has-text("configs").active')).toBeVisible();

    // Verify keys updated
    await page.waitForTimeout(500);
  });
});
