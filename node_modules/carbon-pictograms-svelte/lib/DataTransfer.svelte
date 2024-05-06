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
  <path d="M16,29.36c-7.083,0-12.897-5.542-13.333-12.518	l-1.412,1.412l-0.509-0.51L3,15.491l2.254,2.254l-0.509,0.51l-1.354-1.354C3.855,23.452,9.333,28.64,16,28.64	c4.73,0,9.028-2.607,11.216-6.806l0.639,0.332C25.542,26.604,21,29.36,16,29.36z M16,23.36c-4.058,0-7.36-3.302-7.36-7.36	S11.942,8.64,16,8.64c4.059,0,7.36,3.302,7.36,7.36C23.36,20.059,20.059,23.36,16,23.36z M16,9.36c-3.661,0-6.64,2.979-6.64,6.64	s2.979,6.64,6.64,6.64s6.64-2.979,6.64-6.64S19.661,9.36,16,9.36z M29,16.509l-2.255-2.255l0.51-0.509l1.354,1.354	C28.145,8.548,22.667,3.36,16,3.36c-4.73,0-9.028,2.608-11.216,6.807L4.145,9.833C6.458,5.396,11,2.64,16,2.64	c7.083,0,12.897,5.542,13.334,12.517l1.411-1.412l0.51,0.509L29,16.509z"></path>
</svg>