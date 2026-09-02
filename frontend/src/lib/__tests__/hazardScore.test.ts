import { describe, expect, it } from 'vitest';
import {
  computeHazardScore,
  DEFAULT_SENSOR_RANGES,
  getRiskLevel,
  getSensorContribution,
  normalize,
} from '../hazardScore';

describe('hazard score utilities', () => {
  it('normalizes and clamps values to 0-100', () => {
    expect(normalize(20, 20, 50)).toBe(0);
    expect(normalize(50, 20, 50)).toBe(100);
    expect(normalize(80, 20, 50)).toBe(100);
    expect(normalize(10, 20, 50)).toBe(0);
  });

  it('computes a bounded weighted score', () => {
    expect(computeHazardScore(300, 200, 20)).toBe(0);
    expect(computeHazardScore(1000, 800, 50)).toBe(100);
  });

  it('classifies the documented risk levels at their boundaries', () => {
    expect(getRiskLevel(29.99)).toBe('SAFE');
    expect(getRiskLevel(30)).toBe('WARNING');
    expect(getRiskLevel(59.99)).toBe('WARNING');
    expect(getRiskLevel(60)).toBe('DANGER');
  });

  it('reports a weighted sensor contribution', () => {
    const contribution = getSensorContribution(650, 'mq135', DEFAULT_SENSOR_RANGES);
    expect(contribution.normalized).toBeCloseTo(50);
    expect(contribution.weight).toBe(0.6);
    expect(contribution.contribution).toBeCloseTo(30);
  });
});
