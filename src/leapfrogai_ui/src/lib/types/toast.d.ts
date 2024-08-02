type ToastKind = 'success' | 'info' | 'warning' | 'error';

type ToastNotificationProps = {
  id?: string;
  kind: ToastKind;
  title: string;
  subtitle?: string;
  timeout?: number; // milliseconds
};

type ToastStore = {
  toasts: ToastNotificationProps[];
};
