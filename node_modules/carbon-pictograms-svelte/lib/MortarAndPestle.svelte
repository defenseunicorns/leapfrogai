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
  <path d="M15.982,30.36C7.522,30.36,0.64,23.47,0.64,15c0-0.199,0.161-0.36,0.36-0.36h5.647L2.049,6.678	c-0.447-0.774-0.565-1.68-0.333-2.549s0.788-1.594,1.562-2.041c1.604-0.926,3.664-0.375,4.59,1.229l6.536,11.323H31	c0.199,0,0.36,0.161,0.36,0.36C31.36,23.47,24.462,30.36,15.982,30.36z M1.364,15.36c0.191,7.907,6.675,14.28,14.618,14.28	c7.962,0,14.461-6.373,14.654-14.28H1.364z M7.479,14.64h6.093L7.245,3.678C6.517,2.417,4.899,1.983,3.639,2.711	c-0.608,0.351-1.044,0.92-1.227,1.604c-0.183,0.683-0.09,1.395,0.26,2.002L7.479,14.64z"></path>
</svg>