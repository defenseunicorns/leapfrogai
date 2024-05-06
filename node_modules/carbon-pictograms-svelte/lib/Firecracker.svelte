<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M10,31.36c-0.092,0-0.184-0.035-0.254-0.105l-6-6	c-0.141-0.141-0.141-0.369,0-0.51l14-14c0.141-0.141,0.369-0.141,0.51,0L21,13.491l2.417-2.417c1.419-1.419,1.419-3.729,0-5.148	l-0.672-0.671l0.51-0.51l0.672,0.671c1.698,1.7,1.698,4.467,0,6.167L21.509,14l2.746,2.746c0.141,0.141,0.141,0.369,0,0.509l-14,14	C10.184,31.325,10.092,31.36,10,31.36z M4.509,25L10,30.491L11.491,29L6,23.509L4.509,25z M6.509,23L12,28.491l0.991-0.991	L7.5,22.009L6.509,23z M8.009,21.5l5.491,5.491L23.491,17L18,11.509L8.009,21.5z M21.745,4.254L20.5,3.009l-1.245,1.245l-0.51-0.509	L19.991,2.5l-1.246-1.246l0.51-0.509L20.5,1.991l1.245-1.245l0.51,0.509L21.009,2.5l1.246,1.246L21.745,4.254z"></path>
</svg>