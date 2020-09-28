--
-- PostgreSQL database dump
--

-- Dumped from database version 11.3
-- Dumped by pg_dump version 11.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, password, email, registered_on) FROM stdin;
1	yyy	yyy	yyy@gmail.com	2020-03-19 20:05:51.673546
\.


--
-- Data for Name: general_txt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.general_txt (id, author_id, type, gt_type, title, body, color_txt, color, selected, hide, e_name, h_name) FROM stdin;
251	1	status	Status	Not assigned yet	default	\N	#ff0000	f	f	\N	\N
284	1	accupation	Accupation	Teacher	default	\N	\N	f	f	\N	\N
261	1	weakness	Weakness	Weakness	profile	red	#ff0000	f	f	\N	\N
311	1	profile	Profile	Humptys Profile	0	\N	\N	f	f	\N	\N
257	1	tag	Tag	Sport	ספורט	\N	\N	f	f	\N	\N
253	1	status	\N	achieved	achieved	\N	#00b300	f	f	\N	\N
254	1	subject	Subject	Math	מתמטיקה	\N	\N	f	f	\N	\N
252	1	status	Status	Not yet	Not yet	\N	#ffcccc	f	f	\N	\N
255	1	tag	Tag	English	default	\N	\N	f	f	\N	\N
259	1	category	\N	Subject	profile	blue	#0000cc	f	f	\N	\N
260	1	category	\N	Strength	profile	green	#00b300	f	f	\N	\N
\.


--
-- Data for Name: accupation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accupation (id) FROM stdin;
284
\.


--
-- Data for Name: age_range; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.age_range (id, from_age, to_age) FROM stdin;
\.


--
-- Data for Name: destination; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.destination (id) FROM stdin;
\.


--
-- Data for Name: resource; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.resource (id, type, author_id, title, body, selected, hide) FROM stdin;
\.


--
-- Data for Name: document; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.document (id) FROM stdin;
\.


--
-- Data for Name: general_txt_resource; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.general_txt_resource (general_txt_id, resource_id, title, selected, hide) FROM stdin;
\.


--
-- Data for Name: goal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.goal (id) FROM stdin;
\.


--
-- Data for Name: menta_db; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menta_db (id) FROM stdin;
\.


--
-- Data for Name: migrate_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.migrate_version (repository_id, repository_path, version) FROM stdin;
database repository	C:\\Users\\yasmi\\Documents\\menta4\\db_repository	356
\.


--
-- Data for Name: parent_child_relationship; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.parent_child_relationship (parent_id, child_id) FROM stdin;
254	254
\.


--
-- Data for Name: profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.profile (id) FROM stdin;
311
\.


--
-- Data for Name: psps_db; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.psps_db (id) FROM stdin;
\.


--
-- Data for Name: ufile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ufile (id, author_id, name, data, body, selected, hide) FROM stdin;
\.


--
-- Data for Name: resource_ufile_relationships; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.resource_ufile_relationships (resource_id, ufile_id) FROM stdin;
\.


--
-- Data for Name: student; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.student (id, first_name, last_name, birth_date, grade, background, author_id, registered_on, selected, hide) FROM stdin;
111	111 f	111 l	2001-01-01	1	111111111111111111111111111111111111111111111	\N	2020-03-20	f	f
777	777	777 first	2007-07-07	7	777777777777777777777777777777777777777777777777777777777777777	\N	2020-04-01	f	f
0	Humpty	Dumpty	2020-03-20	D	\N	\N	2020-03-20	f	t
555	std 555 first	std 555 last	2005-05-05	5	55555555555555555555555555555555555555555555555555555	\N	2020-03-30	f	f
8888	std 888	std 888	2008-08-08	8	888888888888888888888888888888888888888888888888888888888888888888	1	2020-04-11	f	f
444	std 444 first	std 444 last	2004-04-04	4	44444444444444444444444444444444444444444444444444444444	\N	2020-03-30	f	f
333	std f 333	std l 333	2003-03-03	3	33333333333333333333333333333333333	\N	2020-03-20	f	f
666	666 first	666 last	2006-06-06	6	666666666666666666666666666666666666666666666666666666666666666666	\N	2020-04-01	f	f
\.


--
-- Data for Name: teacher; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teacher (id, first_name, last_name, birth_date, email, author_id, registered_on, profetional, selected, hide) FROM stdin;
222	t 222 f	t 222 l	0002-02-22 00:00:00	t222@gmail.com	\N	2020-03-20	2	t	f
\.


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role (student_id, teacher_id, title, selected) FROM stdin;
\.


--
-- Data for Name: school; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.school (id) FROM stdin;
\.


--
-- Data for Name: scrt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.scrt (id) FROM stdin;
\.


--
-- Data for Name: status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.status (id) FROM stdin;
251
252
253
\.


--
-- Data for Name: std_general_txt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.std_general_txt (student_id, general_txt_id, due_date, status_id, acc_id, scrt_id, editable, selected, hide) FROM stdin;
0	311	2020-04-14	251	284	\N	t	f	f
111	254	2020-04-14	251	284	\N	t	f	f
\.


--
-- Data for Name: std_resource; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.std_resource (student_id, resource_id, title, body, selected, hide, gt_id, goal_id, who_id, who_title, status_id, status_title, status_color, due_date) FROM stdin;
\.


--
-- Data for Name: strength; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.strength (id) FROM stdin;
\.


--
-- Data for Name: subject; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subject (id) FROM stdin;
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tag (id) FROM stdin;
254
255
257
\.


--
-- Data for Name: todo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.todo (id) FROM stdin;
\.


--
-- Data for Name: weakness; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.weakness (id) FROM stdin;
\.


--
-- Name: general_txt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.general_txt_id_seq', 315, true);


--
-- Name: menta_db_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.menta_db_id_seq', 1, false);


--
-- Name: psps_db_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.psps_db_id_seq', 1, false);


--
-- Name: resource_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.resource_id_seq', 1, false);


--
-- Name: student_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.student_id_seq', 1, false);


--
-- Name: teacher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.teacher_id_seq', 1, false);


--
-- Name: ufile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ufile_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

