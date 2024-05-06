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
  <path d="M27.5,30.36c-1.577,0-2.86-1.283-2.86-2.86c0-0.659,0.225-1.267,0.601-1.751	l-2.424-2.424c-0.76,0.646-1.743,1.035-2.816,1.035c-2.404,0-4.36-1.956-4.36-4.36s1.956-4.36,4.36-4.36s4.36,1.956,4.36,4.36	c0,1.073-0.39,2.057-1.035,2.816l2.424,2.424c0.484-0.376,1.092-0.601,1.751-0.601c1.577,0,2.86,1.283,2.86,2.86	S29.077,30.36,27.5,30.36z M27.5,25.36c-1.18,0-2.14,0.96-2.14,2.14s0.96,2.14,2.14,2.14s2.14-0.96,2.14-2.14	S28.68,25.36,27.5,25.36z M20,16.36c-2.007,0-3.64,1.633-3.64,3.64s1.633,3.64,3.64,3.64s3.64-1.633,3.64-3.64	S22.007,16.36,20,16.36z M15.819,30.311l-12-7C3.708,23.246,3.64,23.128,3.64,23V9h0.72v13.793l11.821,6.896L15.819,30.311z M8.36,16H7.64V6h0.72V16z M28.36,15h-0.72V9.207L16,2.417l-3.64,2.116V13h-0.72V4.325c0-0.128,0.068-0.247,0.179-0.311l4-2.325	c0.112-0.065,0.251-0.065,0.362,0l12,7C28.292,8.753,28.36,8.872,28.36,9V15z"></path>
</svg>