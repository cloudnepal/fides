import React, { createContext, ReactNode, useContext, useMemo } from "react";

import { SystemHistory } from "~/types/api/models/SystemHistory";

type FormType = "before" | "after";

interface SelectedHistoryContextProps {
  selectedHistory: SystemHistory | null;
  formType: FormType;
}

const SelectedHistoryContext =
  createContext<SelectedHistoryContextProps | null>(null);

export const useSelectedHistory = () => useContext(SelectedHistoryContext)!;

interface SelectedHistoryProviderProps {
  children: ReactNode;
  selectedHistory: SystemHistory | null;
  formType: FormType;
}

const SelectedHistoryProvider: React.FC<SelectedHistoryProviderProps> = ({
  children,
  selectedHistory,
  formType,
}) => {
  const value = useMemo(
    () => ({ selectedHistory, formType }),
    [selectedHistory, formType]
  );

  return (
    <SelectedHistoryContext.Provider value={value}>
      {children}
    </SelectedHistoryContext.Provider>
  );
};

export default SelectedHistoryProvider;
