/**
 * Helpers for the fellow display-name -> fellow id lookup that several
 * pages need to turn an author byline into a profile link.
 *
 * Pages either iterate over a collection of fellows once (and call
 * `buildFellowByName`) or receive a serialised plain object via
 * `getStaticPaths` props (since `Map` doesn't survive serialisation).
 * Both consumers share the same shape with `lookup`.
 */

import { getCollection } from 'astro:content';
import type { CollectionEntry } from 'astro:content';

export type FellowByName = Map<string, string>;
export type FellowByNameRecord = Record<string, string>;

export function buildFellowByName(fellows: CollectionEntry<'fellows'>[]): FellowByName {
  return new Map(fellows.map((f) => [f.data.name, f.id]));
}

export function fellowByNameRecord(
  fellows: CollectionEntry<'fellows'>[],
): FellowByNameRecord {
  return Object.fromEntries(fellows.map((f) => [f.data.name, f.id]));
}

/**
 * Resolve once and return both shapes. Useful in routes that need the
 * Map for local logic and also want to forward the plain record into
 * page props.
 */
export async function loadFellowByName(): Promise<{
  map: FellowByName;
  record: FellowByNameRecord;
}> {
  const fellows = await getCollection('fellows');
  const record = fellowByNameRecord(fellows);
  return { map: new Map(Object.entries(record)), record };
}

/**
 * Accept either shape (Map or plain Record) and look up an id.
 */
export function lookupFellowId(
  fellowByName: FellowByName | FellowByNameRecord | undefined,
  name: string,
): string | null {
  if (!fellowByName) return null;
  if (fellowByName instanceof Map) {
    return fellowByName.get(name) ?? null;
  }
  return fellowByName[name] ?? null;
}
