/**
 * Tests for Canonical 4-Tier Severity and Color Mappings
 */
import { getCanonicalSeverity, getRiskLevel, getRiskColor, computeHazardScore } from '../hazardScore';

describe('Canonical 4-Tier Hazard Severity', () => {
  it('correctly maps scores to 4 canonical tiers', () => {
    expect(getCanonicalSeverity(10)).toBe('LOW');
    expect(getCanonicalSeverity(35)).toBe('MEDIUM');
    expect(getCanonicalSeverity(60)).toBe('HIGH');
    expect(getCanonicalSeverity(90)).toBe('CRITICAL');
  });

  it('maintains legacy 3-tier risk mapping', () => {
    expect(getRiskLevel(20)).toBe('SAFE');
    expect(getRiskLevel(45)).toBe('WARNING');
    expect(getRiskLevel(80)).toBe('DANGER');
  });

  it('assigns correct semantic colors across both systems', () => {
    expect(getRiskColor('LOW')).toBe('text-green-500');
    expect(getRiskColor('SAFE')).toBe('text-green-500');
    expect(getRiskColor('MEDIUM')).toBe('text-yellow-500');
    expect(getRiskColor('WARNING')).toBe('text-yellow-500');
    expect(getRiskColor('HIGH')).toBe('text-orange-500');
    expect(getRiskColor('CRITICAL')).toBe('text-red-500');
    expect(getRiskColor('DANGER')).toBe('text-red-500');
  });
});
