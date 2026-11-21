import { test, expect } from '@playwright/test';

test('fluxo demonstrativo até análise', async ({ page }) => {
  await page.goto('/');
  await page.getByRole('link', { name: /use agora/i }).click();
  await page.getByRole('link', { name: /usar fábrica/i }).click();
  await page.getByLabel('Nome').fill('Ada');
  await page.getByLabel('E-mail').fill('ada@malum.test');
  await page.getByLabel('Senha').fill('segredo');
  await page.getByRole('button', { name: /ir para minha análise/i }).click();
  await page.waitForURL('**/app');
  await page.getByLabel('Selecionar planilha').setInputFiles({ name: 'demo.csv', mimeType: 'text/csv', buffer: Buffer.from('data,energia_kwh\n2026-01-01,10') });
  await page.getByRole('button', { name: /continuar/i }).click();
  await page.getByRole('button', { name: /onde estou perdendo/i }).click();
  await page.getByRole('button', { name: /analisar agora/i }).click();
  await expect(page.getByText('Visão de desperdício')).toBeVisible({ timeout: 8000 });
  await page.getByRole('button', { name: 'Linha' }).click();
  await expect(page.getByText('Variação do consumo')).toBeVisible();
  await page.getByRole('button', { name: 'Pizza' }).click();
  await expect(page.getByText('Participação dos recursos')).toBeVisible();
  await page.getByRole('button', { name: 'Histograma' }).click();
  await expect(page.getByText('Desvios da referência')).toBeVisible();
});
