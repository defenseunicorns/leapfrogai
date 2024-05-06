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
  <path d="M24,27.36H10c-5.161,0-9.36-4.199-9.36-9.36c0-5.162,4.199-9.36,9.36-9.36	c0.483,0,0.984,0.042,1.493,0.125C13.092,6.776,15.452,5.64,18,5.64c4.278,0,7.804,3.152,8.298,7.372	C29.29,13.995,31.36,16.834,31.36,20C31.36,24.059,28.059,27.36,24,27.36z M10,9.359c-4.764,0-8.64,3.876-8.64,8.641	c0,4.764,3.876,8.64,8.64,8.64h14c3.661,0,6.64-2.979,6.64-6.64c0-2.93-1.964-5.549-4.776-6.37	c-0.143-0.042-0.245-0.166-0.258-0.314C25.253,9.351,21.983,6.359,18,6.359c-2.395,0-4.608,1.099-6.071,3.016	c-0.083,0.108-0.219,0.157-0.352,0.136C11.03,9.409,10.514,9.359,10,9.359z M24,22.36H14v-0.72h10V22.36z M12,22.36H8v-0.72h4V22.36	z M26,19.36H16v-0.72h10V19.36z M14,19.36H6v-0.72h8V19.36z M24,16.36h-4v-0.72h4V16.36z M18,16.36H8v-0.72h10V16.36z"></path>
</svg>