type ToastKind = 'success' | 'info' | 'warning' | 'error';

type ToastNotificationProps = {
  id?: string;
  kind: ToastKind;
  title: string;
  subtitle?: string;
  timeout?: number; // milliseconds, set to -1 for no expiration
  variant?: 'default' | 'assistant-progress';
  fileIds?: string[]; // required for assistant-progress variant
  vectorStoreId?: string; // required for assistant-progress variant
};

type ToastStore = {
  toasts: ToastNotificationProps[];
};

type ToastData = {
  kind: ToastKind;
  title: string;
  subtitle?: string;
};
