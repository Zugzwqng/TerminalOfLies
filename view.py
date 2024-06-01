import flet as ft
import games_list
import flet_core.page
import flet_test_3



def createGamesList(createdGames: list[str], archivedGames: list[str]) -> ft.Card:
    currentGamesListView = ft.ListView(expand=0, spacing=10, padding=20, height=300, width=230)
    for game in createdGames:
        currentGamesListView.controls.append(ft.Text(game))
    archivedGamesListView = ft.ListView(expand=0, spacing=10, padding=20, height=300, width=250) 
    for game in archivedGames:
        archivedGamesListView.controls.append(ft.Text(game))
        
    lists_of_games = ft.Card(
        content=ft.Container(
            width=500,
            content=ft.Column(
                [
                    ft.Row(
                    [
                        ft.Text("  Current Games"), ft.Text("Archived Games  "), ft.Text("")

                    ]
                    , alignment=ft.MainAxisAlignment.SPACE_BETWEEN

                    ),

                    ft.Row(
                        [
                        currentGamesListView,

                        archivedGamesListView
                        ]
                    ),
                    
                ],
                scroll=ft.ScrollMode.ALWAYS,
                spacing=0,
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            ),
            padding=ft.padding.symmetric(vertical=10),
            alignment=ft.alignment.center
        )
    )
    return lists_of_games


abbreviations_to_alignments = {
    "M" : "Mafia",
    "T" : "Town",
    "N" : "Neutral",
    "H" : "Host",
    "U" : "Unknown",
    "m" : "Mafia (default)",
    "t" : "Town (default)",
    "n" : "Neutral (default)",
    "h" : "Host (default)",
    "u" : "Unknown (default)",
}


def createPlayerlist(players: list[str]) -> ft.SafeArea:
    playerlist = list(map(lambda x : x.split(" | "), players))
    playerlist = list(map(lambda x : [abbreviations_to_alignments[x[0].replace(" ", '')], x[1], x[2]], playerlist))
    dataTable = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Alignment")),
            ft.DataColumn(ft.Text("Players")),
            ft.DataColumn(ft.Text("Aliases")),

        ],
        rows=[ft.DataRow(cells= [ft.DataCell(ft.Text(playerlist[i][0])), 
                                 ft.DataCell(ft.Text(playerlist[i][1])), 
                                 ft.DataCell(ft.Text(playerlist[i][2])),
                                
                                ]) for i in range(len(playerlist))],
        width=600
)
    column = ft.Column(
        controls=[
            ft.Container(content= ft.Column(
                [ft.Row([dataTable], 
                        scroll= ft.ScrollMode.ALWAYS, 
                        alignment = ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        )], 
                scroll= ft.ScrollMode.ALWAYS
            ), expand= 2), 
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
    )
    result = ft.SafeArea(column, expand= True, width=800, height=450)
    return result
    

def createNumberedList(items: list[str], one_index=False, height=300, visible=True) -> ft.Card:
    lv = ft.ListView(expand=0, spacing=10, padding=20, height=height, width=500)
    for i, item in enumerate(items):
        lv.controls.append(ft.Text(f"{i + one_index}: {item}"))
    
    result = ft.Card(
        content=ft.Container(
            width=500,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            lv
                        ]
                    ),
                    
                ],
                scroll=ft.ScrollMode.ALWAYS,
                spacing=0,
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            ),
            padding=ft.padding.symmetric(vertical=10),
            alignment=ft.alignment.center
        ),
        visible=visible
    )
    return result