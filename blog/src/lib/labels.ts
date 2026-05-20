/**
 * Centralised label maps for enum-like fields the schemas use.
 *
 * Each maps an internal token to a human-facing string. Pages should
 * import the relevant `label` helper rather than redefining their own
 * dictionary, so a rename in one place propagates everywhere.
 */

export const rankLabel: Record<string, string> = {
  postulant: 'Postulant',
  novice: 'Novice',
  junior_fellow: 'Junior Fellow',
  fellow: 'Fellow',
  senior_fellow: 'Senior Fellow',
  emeritus: 'Emeritus',
};

// Plural form for cohort tables (dashboard).
export const rankLabelPlural: Record<string, string> = {
  postulant: 'Postulants',
  novice: 'Novices',
  junior_fellow: 'Junior Fellows',
  fellow: 'Fellows',
  senior_fellow: 'Senior Fellows',
  emeritus: 'Emeriti',
};

export const recommendationLabel: Record<string, string> = {
  accept: 'Accept',
  minor: 'Accept with minor revisions',
  major: 'Major revisions required',
  reject: 'Reject',
};

export const roleLabel: Record<string, string> = {
  primary: 'Primary reviewer',
  secondary: 'Secondary reviewer',
  outside: 'Outside reviewer',
};

export const decisionKindLabel: Record<string, string> = {
  bootstrap: 'Founding',
  admission: 'Admission',
  promotion: 'Promotion',
  promotion_review: 'Promotion review',
  release: 'Release',
  andon_cord_pulled: 'Andon cord pulled',
  andon_cord_outcome: 'Andon ruling',
  editorial_ruling: 'Editorial ruling',
  charter_violation_termination: 'Termination (Charter)',
};

export const correctionSeverityLabel: Record<string, string> = {
  typo: 'Typo',
  clarification: 'Clarification',
  factual: 'Factual',
  retraction: 'Retraction',
};

export function labelFor(
  table: Record<string, string>,
  key: string | undefined | null,
): string {
  if (!key) return '';
  return table[key] ?? key;
}
