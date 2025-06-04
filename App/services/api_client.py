import httpx
from typing import Dict, Any, Optional, List, Union
from fastapi import HTTPException

class NFLApiClient:
    """
    Client for interacting with the cached NFL API endpoints
    """
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def get_teams(self) -> List[Dict[str, Any]]:
        """Get all NFL teams through the cached API endpoint"""
        # Use _get directly as this endpoint returns a list
        return await self._get("/nfl/teams")
    
    async def get_schedule(self) -> Dict[str, Any]:
        """Get NFL schedule through the cached API endpoint"""
        return await self._get_with_fallback(f"/nfl/schedule")
    
    async def get_standings(self) -> Dict[str, Any]:
        """Get standings through the cached API endpoint"""
        return await self._get_with_fallback(f"/nfl/standings")
    
    async def get_weekly_injuries(self, season=None, week=None) -> Dict[str, Any]:
        """Get weekly injuries through the cached API endpoint"""
        params = {}
        if season is not None:
            params["season"] = season
        if week is not None:
            params["week"] = week
        return await self._get_with_fallback(f"/nfl/injuries", params)
    
    # New Fantasy Nerds API methods
    
    async def get_draft_rankings(self, format: str = "std") -> Dict[str, Any]:
        """Get draft rankings through the cached API endpoint"""
        params = {"format": format} if format != "std" else {}
        return await self._get_with_fallback("/nfl/draft-rankings", params)
    
    async def get_player_tiers(self, format: str = "std") -> Dict[str, Any]:
        """Get player tiers through the cached API endpoint"""
        params = {"format": format} if format != "std" else {}
        return await self._get_with_fallback("/nfl/player-tiers", params)
    
    async def get_auction_values(self, teams: int = 12, budget: int = 200, format: str = "std") -> Dict[str, Any]:
        """Get auction values through the cached API endpoint"""
        params = {}
        if teams != 12:
            params["teams"] = teams
        if budget != 200:
            params["budget"] = budget
        if format != "std":
            params["format"] = format
        return await self._get_with_fallback("/nfl/auction-values", params)
    
    async def get_adp(self, teams: int = 12, format: str = "std") -> Dict[str, Any]:
        """Get average draft position through the cached API endpoint"""
        params = {}
        if teams != 12:
            params["teams"] = teams
        if format != "std":
            params["format"] = format
        return await self._get_with_fallback("/nfl/adp", params)
    
    async def get_best_ball_rankings(self) -> Dict[str, Any]:
        """Get best ball rankings through the cached API endpoint"""
        return await self._get_with_fallback("/nfl/best-ball")
    
    async def get_bye_weeks(self) -> Dict[str, Any]:
        """Get bye weeks through the cached API endpoint"""
        return await self._get_with_fallback("/nfl/bye-weeks")
    
    async def get_defensive_rankings(self) -> Dict[str, Any]:
        """Get defensive rankings through the cached API endpoint"""
        return await self._get_with_fallback("/nfl/defense-rankings")
    
    async def get_depth_charts(self) -> Dict[str, Any]:
        """Get depth charts through the cached API endpoint"""
        return await self._get_with_fallback("/nfl/depth")
    
    async def get_weekly_projections(self) -> Dict[str, Any]:
        """Get weekly projections through the cached API endpoint"""
        return await self._get_with_fallback("/nfl/weekly-projections")
    
    async def get_weekly_rankings(self, format: str = "std") -> Dict[str, Any]:
        """Get weekly rankings through the cached API endpoint"""
        params = {"format": format} if format != "std" else {}
        return await self._get_with_fallback("/nfl/weekly-rankings", params)
    
    async def get_dynasty_rankings(self) -> Dict[str, Any]:
        """Get dynasty rankings through the cached API endpoint"""
        return await self._get_with_fallback("/nfl/dynasty")
    
    async def get_nfl_news(self) -> List[Dict[str, Any]]:
        """Get NFL news through the cached API endpoint"""
        # Use _get directly as this endpoint returns a list
        return await self._get("/nfl/news")
    
    async def get_fantasy_leaders(self, format: str = "std", position: str = "ALL", week: int = 0) -> Dict[str, Any]:
        """Get fantasy leaders through the cached API endpoint"""
        params = {}
        if format != "std":
            params["format"] = format
        if position != "ALL":
            params["position"] = position
        if week != 0:
            params["week"] = week
        return await self._get_with_fallback("/nfl/fantasy-leaders", params)
    
    async def get_players(self, include_inactive: bool = False) -> Dict[str, Any]:
        """Get NFL players through the cached API endpoint"""
        params = {}
        if include_inactive:
            params["include_inactive"] = 1
        return await self._get_with_fallback("/nfl/players", params)
    
    async def get_player_adds_drops(self) -> Dict[str, Any]:
        """Get player adds and drops through the cached API endpoint"""
        return await self._get_with_fallback("/nfl/add-drops")
        
    async def get_weather_forecasts(self) -> Dict[str, Any]:
        """Get weather forecasts through the cached API endpoint"""
        return await self._get_with_fallback("/nfl/weather")
        
    async def get_draft_projections(self) -> Dict[str, Any]:
        """Get draft projections through the cached API endpoint"""
        return await self._get_with_fallback("/nfl/draft-projections")
        
    async def get_rest_of_season_projections(self) -> Dict[str, Any]:
        """Get rest of season projections through the cached API endpoint"""
        return await self._get_with_fallback("/nfl/ros")
    
    async def _get(self, endpoint: str, params: Dict[str, Any] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a GET request to the API
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            JSON response (can be a dictionary or a list)
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            detail = f"API error {status_code}: {str(e)}"
            raise HTTPException(status_code=status_code, detail=detail)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error accessing API: {str(e)}")
    
    async def _get_with_fallback(self, endpoint: str, params: Dict[str, Any] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a GET request to the API
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            JSON response directly from the Fantasy Nerds API
        """
        response = await self._get(endpoint, params)
        return response
    
    async def close(self):
        """Close the HTTP client connection"""
        await self.client.aclose()

# Create a singleton instance
nfl_api_client = NFLApiClient()
