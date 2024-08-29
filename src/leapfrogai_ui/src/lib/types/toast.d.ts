type ToastKind = 'success' | 'info' | 'warning' | 'error';

type ToastNotificationProps = {
  id?: string;
  kind: ToastKind;
  title: string;
  subtitle?: string;
  timeout?: number; // milliseconds, set to -1 for no expiration
  vectorStoreId?: string; // for showing assistant file vectorization progress
};

type ToastStore = {
  toasts: ToastNotificationProps[];
};
