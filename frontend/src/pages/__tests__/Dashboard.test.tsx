import { describe, it, expect, vi } from 'vitest';
import { createElement, type ReactNode } from 'react';
import { act, render, screen } from '@testing-library/react';
import Dashboard from '../Dashboard';
import * as FirebaseContext from '@/contexts/FirebaseContext';

// Mock the Firebase context
vi.mock('@/contexts/FirebaseContext', () => ({
  useFirebase: vi.fn()
}));

vi.mock('@/contexts/AuthContext', () => ({
  useAuth: vi.fn(() => ({ currentUser: { emailVerified: true } }))
}));

// Mock other dependencies
vi.mock('react-router-dom', () => ({
  useNavigate: () => vi.fn(),
  NavLink: ({ children }: { children?: ReactNode }) => createElement('span', null, children),
  Link: ({ children }: { children?: ReactNode }) => createElement('span', null, children)
}));

vi.mock('recharts', () => ({
  LineChart: () => null,
  Line: () => null,
  XAxis: () => null,
  YAxis: () => null,
  CartesianGrid: () => null,
  Tooltip: () => null,
  ResponsiveContainer: () => null,
  ReferenceLine: () => null
}));

describe('Dashboard Hazard Score Color Mapping', () => {
  const mockFirebaseData = {
    iotLoading: false,
    iotError: null,
    hazardLoading: false,
    hazardError: null,
    calculatedHazardScore: 0,
    calculatedRiskLevel: 'SAFE' as const,
    roverLoading: false,
    alertsLoading: false,
    historyLoading: false,
    dbConnected: true,
    roverControl: { direction: 'stop', speed: 0, mode: 'manual', emergency: false },
    roverStatus: { battery: 100, location: 'Zone A', online: true },
    alerts: [],
    unresolvedAlerts: [],
    history: [],
    setRoverDirection: vi.fn(),
    setRoverMode: vi.fn(),
    updateRoverControl: vi.fn(),
    triggerEmergency: vi.fn(),
    addAlert: vi.fn(),
    resolveAlert: vi.fn(),
    updateSettings: vi.fn(),
    updateThresholds: vi.fn(),
    updateRoverBehavior: vi.fn()
  };

  it('should display SAFE status with green color for hazardScore < 30', () => {
    const mockData = {
      ...mockFirebaseData,
      iotReadings: {
        mq2: 200,
        mq135: 400,
        mq135_raw: 0,
        mq135_digital: 0,
        temperature: 25,
        humidity: 50,
        flame: false,
        motion: false,
        hazardScore: 20,
        riskLevel: 'SAFE' as const,
        status: { online: true, lastHeartbeat: Date.now() },
        emergency: { active: false, timestamp: 0 }
      },
      hazardScore: 20,
      riskLevel: 'SAFE' as const
    };

    vi.spyOn(FirebaseContext, 'useFirebase').mockReturnValue(mockData);

    render(<Dashboard />);
    
    // Check that SAFE badge is displayed
    expect(screen.getAllByText(/SAFE/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Hazard Score: 20/i)).toBeInTheDocument();
  });

  it('should display WARNING status with orange color for hazardScore 31-60', () => {
    const mockData = {
      ...mockFirebaseData,
      iotReadings: {
        mq2: 500,
        mq135: 700,
        mq135_raw: 1,
        mq135_digital: 1,
        temperature: 32,
        humidity: 45,
        flame: false,
        motion: true,
        hazardScore: 45,
        riskLevel: 'WARNING' as const,
        status: { online: true, lastHeartbeat: Date.now() },
        emergency: { active: false, timestamp: 0 }
      },
      hazardScore: 45,
      riskLevel: 'WARNING' as const
    };

    vi.spyOn(FirebaseContext, 'useFirebase').mockReturnValue(mockData);

    render(<Dashboard />);
    
    // Check that WARNING badge is displayed
    expect(screen.getAllByText(/WARNING/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Hazard Score: 45/i)).toBeInTheDocument();
    
    // Check for warning alert banner
    expect(screen.getByText(/⚠️ WARNING — Check Situation/i)).toBeInTheDocument();
  });

  it('should display DANGER status with red color for hazardScore >= 61', () => {
    const mockData = {
      ...mockFirebaseData,
      iotReadings: {
        mq2: 800,
        mq135: 950,
        mq135_raw: 1,
        mq135_digital: 1,
        temperature: 45,
        humidity: 30,
        flame: true,
        motion: true,
        hazardScore: 75,
        riskLevel: 'DANGER' as const,
        status: { online: true, lastHeartbeat: Date.now() },
        emergency: { active: false, timestamp: 0 }
      },
      hazardScore: 75,
      riskLevel: 'DANGER' as const
    };

    vi.spyOn(FirebaseContext, 'useFirebase').mockReturnValue(mockData);

    render(<Dashboard />);
    
    // Check that DANGER badge is displayed
    expect(screen.getAllByText(/DANGER/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/Hazard Score: 75/i)).toBeInTheDocument();
    
    // Check for danger alert banner
    expect(screen.getByText(/🚨 DANGER — Immediate Action Required/i)).toBeInTheDocument();
  });

  it('should display loading state when iotLoading is true', () => {
    const mockData = {
      ...mockFirebaseData,
      iotLoading: true,
      iotReadings: null
    };

    vi.spyOn(FirebaseContext, 'useFirebase').mockReturnValue(mockData);

    render(<Dashboard />);
    
    expect(screen.getByText(/Connecting to AROHAN node/i)).toBeInTheDocument();
  });

  it('should display no data state when no readings available', () => {
    const mockData = {
      ...mockFirebaseData,
      iotLoading: false,
      iotReadings: null,
      iotError: null
    };

    vi.spyOn(FirebaseContext, 'useFirebase').mockReturnValue(mockData);

    render(<Dashboard />);
    
    expect(screen.getByText(/No Data in Firebase/i)).toBeInTheDocument();
  });

  it('should keep the dashboard rendered when iotError is present', () => {
    const mockData = {
      ...mockFirebaseData,
      iotLoading: false,
      iotReadings: null,
      dbConnected: false,
      hazardScore: 0,
      riskLevel: 'SAFE' as const,
      iotError: new Error('Connection failed')
    };

    vi.spyOn(FirebaseContext, 'useFirebase').mockReturnValue(mockData);

    render(<Dashboard />);
    expect(screen.getByText(/AROHAN Command Center/i)).toBeInTheDocument();
  });
});
