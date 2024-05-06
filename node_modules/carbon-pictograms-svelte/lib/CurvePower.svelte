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
  <path d="M21.591,27.473L19.109,24h1.276l1.777,2.605h0.041	L24.047,24h1.208l-2.469,3.391L25.308,31h-1.275l-1.818-2.74h-0.041L20.208,31H19L21.591,27.473z M28.704,23h0.688l-1.203,3.525	c-0.149,0.43-0.361,0.613-0.854,0.613h-0.441v-0.584h0.538l0.138-0.419L26.498,23h0.727l0.522,1.582l0.195,0.756h0.035l0.206-0.756	L28.704,23z M16.36,31h-0.72V16.36H1v-0.72h14.64V8.853c-1.198-3.445-1.921-6.478-1.991-6.771l0.701-0.165	c0.277,1.177,0.72,2.828,1.29,4.639V1h0.72v7.723c0.872,2.482,1.936,5.027,3.105,6.917h6.886c2.167-3.883,3.734-10.526,4.295-13.703	l0.709,0.125c-0.087,0.491-1.555,8.642-4.198,13.578H31v0.72h-4.253c-1.076,1.786-2.329,3-3.747,3c-1.414,0-2.736-1.215-3.915-3	H16.36V31z M19.938,16.36c0.976,1.39,2.013,2.28,3.062,2.28c1.047,0,2.029-0.89,2.921-2.28H19.938z M16.36,15.64h2.275	c-0.848-1.428-1.612-3.125-2.275-4.827V15.64z"></path>
</svg>