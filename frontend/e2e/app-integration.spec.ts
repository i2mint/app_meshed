/**
 * E2E Integration Tests - Full Application Flow
 */

import { test, expect } from '@playwright/test';

test.describe('Full Application Integration', () => {
  test('should navigate between all three views', async ({ page }) => {
    await page.goto('/');

    // Start at Mesh Maker (default)
    await expect(page.getByText('Mesh Maker')).toBeVisible();

    // Navigate to Store Browser
    await page.click('button:has-text("Store Browser")');
    await expect(page.getByText('Stores')).toBeVisible();

    // Navigate to Stream Viewer
    await page.click('button:has-text("Stream Viewer")');
    await expect(page.getByText('Streams')).toBeVisible();

    // Back to Mesh Maker
    await page.click('button:has-text("Mesh Maker")');
    await expect(page.getByText('Functions')).toBeVisible();
  });

  test('should have correct header and footer', async ({ page }) => {
    await page.goto('/');

    // Check header
    await expect(page.getByText('app_meshed')).toBeVisible();
    await expect(page.getByText('Modular DAG Composition Platform')).toBeVisible();

    // Check footer
    await expect(page.getByText('Built with React, React Flow, RJSF, and Plotly')).toBeVisible();
    await expect(page.getByText('Backend:')).toBeVisible();
    await expect(page.getByText('localhost:8000')).toBeVisible();
  });

  test('should maintain state when switching views', async ({ page }) => {
    await page.goto('/');
    await page.waitForTimeout(1000);

    // In Mesh Maker, set DAG name
    const dagNameInput = page.locator('input[placeholder="DAG name"]');
    await dagNameInput.clear();
    await dagNameInput.fill('persistent_dag');

    // Switch to Store Browser
    await page.click('button:has-text("Store Browser")');
    await page.waitForTimeout(500);

    // Switch back to Mesh Maker
    await page.click('button:has-text("Mesh Maker")');
    await page.waitForTimeout(500);

    // Check that DAG name persisted
    await expect(dagNameInput).toHaveValue('persistent_dag');
  });

  test('complete workflow: create DAG, save, and execute', async ({ page }) => {
    await page.goto('/');
    await page.waitForTimeout(1500);

    // Step 1: Create a simple DAG
    const dagName = `test_workflow_${Date.now()}`;
    const dagNameInput = page.locator('input[placeholder="DAG name"]');
    await dagNameInput.clear();
    await dagNameInput.fill(dagName);

    // Add an 'add' node
    await page.click('button:has-text("add")');
    await page.waitForTimeout(500);

    // Step 2: Save the DAG
    await page.click('button:has-text("Save")');
    await page.waitForTimeout(1500);

    // Step 3: Execute the DAG
    const inputsTextarea = page.locator('textarea[placeholder*="node_id"]');
    await inputsTextarea.clear();
    await inputsTextarea.fill('{"a": 10, "b": 20}');

    await page.click('button:has-text("Execute")');
    await page.waitForTimeout(2000);

    // Verify execution result appears
    await expect(page.getByText('Result:')).toBeVisible();

    // Step 4: Verify DAG was saved by checking Store Browser
    await page.click('button:has-text("Store Browser")');
    await page.waitForTimeout(500);

    await page.click('button:has-text("meshes")');
    await page.waitForTimeout(1000);

    // The DAG should appear in the list
    await expect(page.getByText(dagName)).toBeVisible();
  });

  test('should handle backend connectivity', async ({ page }) => {
    await page.goto('/');

    // Wait for initial data load
    await page.waitForTimeout(2000);

    // Go to Store Browser - this requires backend
    await page.click('button:has-text("Store Browser")');
    await page.waitForTimeout(1000);

    // If stores are visible, backend is connected
    const storesHeading = page.getByText('Stores');
    await expect(storesHeading).toBeVisible();
  });

  test('should display all navigation tabs', async ({ page }) => {
    await page.goto('/');

    // Check all three navigation tabs are present
    const storeBrowserTab = page.locator('nav button:has-text("Store Browser")');
    const meshMakerTab = page.locator('nav button:has-text("Mesh Maker")');
    const streamViewerTab = page.locator('nav button:has-text("Stream Viewer")');

    await expect(storeBrowserTab).toBeVisible();
    await expect(meshMakerTab).toBeVisible();
    await expect(streamViewerTab).toBeVisible();
  });

  test('should highlight active navigation tab', async ({ page }) => {
    await page.goto('/');

    // Mesh Maker should be active by default
    const meshMakerTab = page.locator('nav button:has-text("Mesh Maker")');
    await expect(meshMakerTab).toHaveClass(/active/);

    // Click Store Browser
    await page.click('button:has-text("Store Browser")');

    // Store Browser should now be active
    const storeBrowserTab = page.locator('nav button:has-text("Store Browser")');
    await expect(storeBrowserTab).toHaveClass(/active/);
  });
});
