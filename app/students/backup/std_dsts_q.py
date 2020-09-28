for d in dsts_not_of_student:
        print("D  NOT_OF_STD ", d.title, d.id)
        for g in goals_not_of_student:
            if d.is_parent_of(g):
                print("   G  NOT_OF_STD", g.title, g.id)
            for t in todos_not_of_student:
                if g.is_parent_of(t):
                    print("       T  NOT_OF_STD", t.title, t.id)