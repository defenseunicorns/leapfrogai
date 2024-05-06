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
  <path d="M23.5,31.36c-0.062,0-0.124-0.017-0.181-0.049	l-7.5-4.336c-0.111-0.064-0.18-0.183-0.18-0.312v-8.672c0-0.129,0.068-0.247,0.18-0.312l7.5-4.336c0.113-0.064,0.248-0.064,0.361,0	l7.5,4.336c0.11,0.064,0.18,0.183,0.18,0.312v8.672c0,0.129-0.069,0.247-0.18,0.312l-7.5,4.336	C23.624,31.344,23.562,31.36,23.5,31.36z M16.36,26.456l7.14,4.128l7.14-4.128V18.2l-7.14-4.128L16.36,18.2V26.456z M13,25.36H9	c-4.61,0-8.36-3.751-8.36-8.36c0-3.818,2.544-7.105,6.217-8.074C7.835,4.111,12.064,0.64,17,0.64c5.713,0,10.36,4.647,10.36,10.36	h-0.72c0-5.315-4.324-9.64-9.64-9.64c-4.666,0-8.651,3.332-9.478,7.923C7.497,9.424,7.39,9.537,7.25,9.57	C3.782,10.384,1.36,13.44,1.36,17c0,4.213,3.427,7.64,7.64,7.64h4V25.36z"></path>
</svg>