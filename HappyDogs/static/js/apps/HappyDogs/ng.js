var angularApp = angular.module('HappyDogs' , ['ngResource']);

angularApp.controller('HappyDogsHomeCalendar' , [ '$scope' , '$resource' , HappyDogsHomeCalendar ]).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

function HappyDogsHomeCalendar($scope, $resource , $http){
    $scope.LoginDisplay = true;
    $scope.DetailDisplay = false;
    $scope.detail_date = '2016/12/12'
	$scope.HappyDogsHomeCalendarResource = $resource(
		'/rest/happy_dogs/home_calendar.json' ,
		{
            start_date : '@start_date' ,
            end_date : '@end_date' ,
		} ,
		{
			get : {
				method : 'JSON'
			} ,
		}
	);
	$scope.HappyDogsHomeCalendarDetailResource = $resource(
		'/rest/happy_dogs/detail_calendar.json' ,
		{
            date : '@start_date' ,
		} ,
		{
			get : {
				method : 'JSON'
			} ,
		}
	);
	$scope.HappyDogsHomeCalendarResource.get().$promise.then(function(data){
		$scope.LoginDisplay = false;
		$scope.weeks = data.data.weeks;
	});
	$scope.HappyDogsHomeCalendarFilterList = function(){
	    $scope.LoginDisplay = true;
        $scope.HappyDogsHomeCalendarResource.get({
            start_date : $scope.start_date ,
            end_date : $scope.end_date
        }).$promise.then(function(data){
            $scope.LoginDisplay = false;
            $scope.weeks = data.data.weeks;
        });
	};
	$scope.HappyDogsHomeCalendarShowDetail = function(date, week){
        $scope.LoginDisplay = true;
        $scope.DetailDisplay = false;
        $scope.HappyDogsHomeCalendarDetailResource.get({
            date : date
        }).$promise.then(function(data){
            $scope.DetailDisplay = true;
            $scope.LoginDisplay = false;
            $scope.day_detail = data.data.detail;
        });
	};
	$scope.HappyDogsHomeCalendarDetailClose = function(){
        $scope.DetailDisplay = false;
        $scope.LoginDisplay = false;
        $scope.day_detail = null;
	}
}