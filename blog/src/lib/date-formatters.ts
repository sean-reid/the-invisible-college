/**
 * Shared Intl.DateTimeFormat instances used across pages.
 *
 * Centralising these saves duplicate instantiation in every route's
 * frontmatter and locks the wording (`en-US`, UTC timezone, long month
 * vs short month) so two pages don't drift apart visually.
 */

export const longDateFormatter = new Intl.DateTimeFormat('en-US', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  timeZone: 'UTC',
});

export const shortDateFormatter = new Intl.DateTimeFormat('en-US', {
  year: 'numeric',
  month: 'short',
  day: 'numeric',
  timeZone: 'UTC',
});

export const monthFormatter = new Intl.DateTimeFormat('en-US', {
  year: 'numeric',
  month: 'long',
  timeZone: 'UTC',
});

export function formatLong(date: Date): string {
  return longDateFormatter.format(date);
}

export function formatShort(date: Date): string {
  return shortDateFormatter.format(date);
}

export function formatMonth(date: Date): string {
  return monthFormatter.format(date);
}
