/**
 * E2E Tests for Stream Viewer (Phase III)
 */

import { test, expect } from '@playwright/test';

test.describe('Stream Viewer', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    // Navigate to Stream Viewer
    await page.click('button:has-text("Stream Viewer")');
    await expect(page.getByText('Streams')).toBeVisible();
  });

  test('should display available streams', async ({ page }) => {
    // Wait for streams to load
    await page.waitForTimeout(1500);

    // Check that streams are listed
    await expect(page.getByText('audio_sample')).toBeVisible();
    await expect(page.getByText('sensor_accel_x')).toBeVisible();
    await expect(page.getByText('sensor_accel_y')).toBeVisible();
  });

  test('should select streams for visualization', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Check a stream checkbox
    const checkbox = page.locator('input[type="checkbox"]').first();
    await checkbox.check();

    // Verify it's checked
    await expect(checkbox).toBeChecked();
  });

  test('should display stream metadata', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Check that metadata is shown (sample rate, duration)
    await expect(page.getByText(/Hz/)).toBeVisible();
    await expect(page.getByText(/s$/)).toBeVisible();  // Duration in seconds
  });

  test('should display plot controls', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Check for zoom controls
    await expect(page.locator('button[title="Zoom In"]')).toBeVisible();
    await expect(page.locator('button[title="Zoom Out"]')).toBeVisible();
    await expect(page.locator('button[title="Refresh"]')).toBeVisible();

    // Check for pan controls
    await expect(page.getByText('Pan Left')).toBeVisible();
    await expect(page.getByText('Pan Right')).toBeVisible();
  });

  test('should display time range information', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Check that time range is displayed
    await expect(page.getByText(/Time:/)).toBeVisible();
    await expect(page.getByText(/Zoom:/)).toBeVisible();
  });

  test('should zoom in on plot', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Get initial zoom level
    const zoomText = await page.getByText(/Zoom: [\d.]+x/).textContent();

    // Click zoom in
    await page.click('button[title="Zoom In"]');

    await page.waitForTimeout(1000);

    // Check that zoom level changed
    const newZoomText = await page.getByText(/Zoom: [\d.]+x/).textContent();
    expect(newZoomText).not.toBe(zoomText);
  });

  test('should zoom out on plot', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Click zoom out
    await page.click('button[title="Zoom Out"]');

    await page.waitForTimeout(1000);

    // Verify the operation completed
    await expect(page.getByText(/Zoom:/)).toBeVisible();
  });

  test('should pan left', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Get initial time range
    const timeText = await page.getByText(/Time: /).textContent();

    // Click pan left
    await page.click('button:has-text("Pan Left")');

    await page.waitForTimeout(1000);

    // Verify time range changed
    const newTimeText = await page.getByText(/Time: /).textContent();
    expect(newTimeText).not.toBe(timeText);
  });

  test('should pan right', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Click pan right
    await page.click('button:has-text("Pan Right")');

    await page.waitForTimeout(1000);

    // Verify the operation completed
    await expect(page.getByText(/Time:/)).toBeVisible();
  });

  test('should refresh plot data', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Click refresh
    await page.click('button[title="Refresh"]');

    await page.waitForTimeout(1000);

    // Verify page is still functional
    await expect(page.getByText('Streams')).toBeVisible();
  });

  test('should display channel information when streams selected', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Select a stream
    const checkbox = page.locator('input[type="checkbox"]').first();
    if (!(await checkbox.isChecked())) {
      await checkbox.check();
    }

    await page.waitForTimeout(1500);

    // Check for channel info section
    await expect(page.getByText('Channel Information')).toBeVisible();
    await expect(page.getByText(/samples @/)).toBeVisible();
  });

  test('should handle multiple stream selection', async ({ page }) => {
    await page.waitForTimeout(1500);

    // Select multiple streams
    const checkboxes = page.locator('input[type="checkbox"]');
    const count = await checkboxes.count();

    if (count >= 2) {
      await checkboxes.nth(0).check();
      await checkboxes.nth(1).check();

      await page.waitForTimeout(1500);

      // Verify multiple channels are shown
      await expect(page.getByText('Channel Information')).toBeVisible();
    }
  });
});
