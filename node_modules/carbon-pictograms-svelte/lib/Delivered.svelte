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
  <path d="M28,31.36H4c-0.75,0-1.36-0.61-1.36-1.36V9.36H1	C0.801,9.36,0.64,9.199,0.64,9V1c0-0.199,0.161-0.36,0.36-0.36h30c0.199,0,0.36,0.161,0.36,0.36v8c0,0.199-0.161,0.36-0.36,0.36	h-1.64V30C29.36,30.75,28.75,31.36,28,31.36z M3.36,9.36V30c0,0.353,0.287,0.64,0.64,0.64h24c0.353,0,0.64-0.287,0.64-0.64V9.36	H3.36z M1.36,8.64h29.28V1.36H1.36V8.64z M14,23.36c-0.092,0-0.184-0.035-0.254-0.105l-4-4l0.509-0.51L14,22.491l7.745-7.746	l0.51,0.509l-8,8C14.184,23.325,14.092,23.36,14,23.36z"></path>
</svg>