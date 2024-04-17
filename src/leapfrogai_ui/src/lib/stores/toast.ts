import { writable } from 'svelte/store';
import { v4 as uuidv4 } from 'uuid';
import type { ToastNotificationProps } from 'carbon-components-svelte/src/Notification/ToastNotification.svelte';

const defaultValues: ToastStore = {
	toasts: []
};

const toastDefaults: Pick<ToastNotificationProps, 'kind' | 'caption' | 'timeout'> = {
	kind: 'info',
	caption: new Date().toLocaleString(),
	timeout: 3000
};
const createToastsStore = () => {
	const { subscribe, update } = writable<ToastStore>({ ...defaultValues });

	return {
		subscribe,
		addToast: (toast: RequiredToastFields & OptionalToastFields) => {
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
			setTimeout(() => {
				update((old) => ({
					...old,
					toasts: old.toasts.filter((toast) => toast.id !== id)
				}));
			}, newToast.timeout);
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
