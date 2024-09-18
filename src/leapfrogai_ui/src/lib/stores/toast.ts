import { writable } from 'svelte/store';
import { v4 as uuidv4 } from 'uuid';

const defaultValues: ToastStore = {
  toasts: []
};

const toastDefaults: ToastNotificationProps = {
  kind: 'info',
  title: '',
  timeout: 3000,
  variant: 'default'
};
const createToastsStore = () => {
  const { subscribe, update } = writable<ToastStore>({ ...defaultValues });

  return {
    subscribe,
    addToast: (toast: ToastNotificationProps) => {
      const id = uuidv4();
      const newToast: ToastNotificationProps = {
        id,
        ...toastDefaults,
        ...toast
      };
      update((old) => ({
        ...old,
        toasts: [...old.toasts, newToast]
      }));

      // Remove toast after timeout
      if (newToast.timeout !== -1) {
        setTimeout(() => {
          update((old) => ({
            ...old,
            toasts: old.toasts.filter((toast) => toast.id !== id)
          }));
        }, newToast.timeout);
      }
    },
    dismissToast: (id: string) => {
      update((old) => ({
        ...old,
        toasts: old.toasts.filter((toast) => toast.id !== id)
      }));
    }
  };
};

export default createToastsStore();
